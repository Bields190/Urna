import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_eleicao #type:ignore
import m_chapa #type: ignore
import m_voto #type: ignore
from model import Model
from datetime import datetime


class Control:
    def __init__(self, tela=None):
        self.tela = tela

    def adicionar_eleicao(self):
        """Adiciona uma nova eleição"""
        titulo = str(self.tela.entry1.get()).strip()
        data_inicio = self.tela.entry2.entry.get()
        data_fim = self.tela.entry3.entry.get()
        
        if not titulo:
            print("Título é obrigatório!")
            return False
            
        if not data_inicio or not data_fim:
            print("Datas de início e fim são obrigatórias!")
            return False
            
        # Converter formato de data de DD-MM-YYYY para YYYY-MM-DD
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%d-%m-%Y')
            data_fim_obj = datetime.strptime(data_fim, '%d-%m-%Y')
            
            data_inicio_bd = data_inicio_obj.strftime('%Y-%m-%d')
            data_fim_bd = data_fim_obj.strftime('%Y-%m-%d')
            
            # Validar se data de fim é posterior à data de início
            if data_fim_obj <= data_inicio_obj:
                print("Data de fim deve ser posterior à data de início!")
                return False
                
        except ValueError:
            print("Formato de data inválido!")
            return False
            
        eleicao = m_eleicao.Eleicao(titulo, data_inicio_bd, data_fim_bd)
        resultado = eleicao.salvar()
        
        # Se a eleição foi salva com sucesso e há chapas selecionadas
        if resultado and hasattr(self.tela, 'chapas') and self.tela.chapas:
            eleicao_id = eleicao.id
            self.associar_chapas_eleicao(eleicao_id, self.tela.chapas)
            
        return resultado

    def listar_eleicoes(self):
        """Lista todas as eleições"""
        return m_eleicao.Eleicao.listar()

    def atualizar_eleicao(self, id, titulo, data_inicio, data_fim):
        """Atualiza uma eleição existente"""
        if not titulo:
            print("Título é obrigatório!")
            return False
            
        # Converter formato de data se necessário
        try:
            if '-' in data_inicio and len(data_inicio.split('-')[0]) == 2:
                data_inicio_obj = datetime.strptime(data_inicio, '%d-%m-%Y')
                data_inicio = data_inicio_obj.strftime('%Y-%m-%d')
            
            if '-' in data_fim and len(data_fim.split('-')[0]) == 2:
                data_fim_obj = datetime.strptime(data_fim, '%d-%m-%Y')
                data_fim = data_fim_obj.strftime('%Y-%m-%d')
                
            # Validar se data de fim é posterior à data de início
            inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
            if fim_obj <= inicio_obj:
                print("Data de fim deve ser posterior à data de início!")
                return False
                
        except ValueError:
            print("Formato de data inválido!")
            return False
            
        eleicao = m_eleicao.Eleicao(titulo, data_inicio, data_fim, id=id)
        resultado = eleicao.atualizar()
        
        # Se a eleição foi atualizada com sucesso e há chapas selecionadas
        if resultado and hasattr(self.tela, 'chapas') and self.tela.chapas:
            # Primeiro remove todas as associações existentes
            self.remover_chapas_eleicao(id)
            # Depois adiciona as novas associações
            self.associar_chapas_eleicao(id, self.tela.chapas)
            
        return resultado

    def deletar_eleicao(self, id):
        """Deleta uma eleição"""
        eleicao = m_eleicao.Eleicao("", "", "", id=id)
        return eleicao.deletar()

    def buscar_eleicao(self, id):
        """Busca uma eleição por ID"""
        eleicao = m_eleicao.Eleicao("", "", "")
        return eleicao.ver(id)
        
    def obter_status_eleicao(self, data_inicio, data_fim):
        """Determina o status da eleição baseado nas datas"""
        hoje = datetime.now().date()
        
        try:
            # Assumir que as datas estão no formato YYYY-MM-DD do banco
            inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            
            if hoje < inicio:
                return "Agendada"
            elif inicio <= hoje <= fim:
                return "Ativa"
            else:
                return "Encerrada"
                
        except ValueError:
            return "Indefinido"
            
    def formatar_data_exibicao(self, data_bd):
        """Converte data do formato YYYY-MM-DD para DD/MM/YYYY para exibição"""
        try:
            data_obj = datetime.strptime(data_bd, '%Y-%m-%d')
            return data_obj.strftime('%d/%m/%Y')
        except ValueError:
            return data_bd

    def validar_eleicao_ativa(self, id):
        """Verifica se uma eleição está ativa (para operações específicas)"""
        eleicao_data = self.buscar_eleicao(id)
        if eleicao_data:
            _, _, data_inicio, data_fim = eleicao_data[0]
            status = self.obter_status_eleicao(data_inicio, data_fim)
            return status == "Ativa"
        return False

    def pode_editar_eleicao(self, id):
        """Verifica se uma eleição pode ser editada (apenas agendadas)"""
        eleicao_data = self.buscar_eleicao(id)
        if eleicao_data:
            _, _, data_inicio, data_fim = eleicao_data[0]
            status = self.obter_status_eleicao(data_inicio, data_fim)
            return status == "Agendada"
        return False

    def pode_deletar_eleicao(self, id):
        """Verifica se uma eleição pode ser deletada (apenas agendadas)"""
        return self.pode_editar_eleicao(id)

    def encerrar_eleicao(self, id):
        """Encerra uma eleição ativa alterando sua data de fim para hoje"""
        if not self.validar_eleicao_ativa(id):
            print("Apenas eleições ativas podem ser encerradas!")
            return False
            
        eleicao_data = self.buscar_eleicao(id)
        if eleicao_data:
            id_el, titulo, data_inicio, _ = eleicao_data[0]
            hoje = datetime.now().strftime('%Y-%m-%d')
            
            # Atualizar com data de fim sendo hoje
            return self.atualizar_eleicao(id_el, titulo, data_inicio, hoje)
        return False

    def obter_estatisticas_eleicoes(self):
        """Retorna estatísticas das eleições"""
        eleicoes = self.listar_eleicoes()
        
        stats = {
            'total': len(eleicoes),
            'ativas': 0,
            'agendadas': 0,
            'encerradas': 0
        }
        
        for eleicao in eleicoes:
            _, _, data_inicio, data_fim = eleicao
            status = self.obter_status_eleicao(data_inicio, data_fim)
            
            if status == "Ativa":
                stats['ativas'] += 1
            elif status == "Agendada":
                stats['agendadas'] += 1
            elif status == "Encerrada":
                stats['encerradas'] += 1
                
        return stats

    def resultado_eleicao(self, eleicao_id):
        """
        Retorna um dicionário com:
        - total de votos
        - lista de chapas com votos e percentual
        """
        chapas = m_chapa.Chapa.listar_por_eleicao(eleicao_id)
        total_votos = m_voto.Voto.contar_total_eleicao(eleicao_id)
        resultado = []

        for chapa in chapas:
            chapa_id, nome, slogan, logo = chapa
            votos = m_voto.Voto.contar_por_chapa(chapa_id)
            percentual = (votos / total_votos * 100) if total_votos > 0 else 0
            resultado.append({
                "chapa_id": chapa_id,
                "nome": nome,
                "slogan": slogan,
                "logo": logo,
                "votos": votos,
                "percentual": percentual
            })

        # Ordenar do maior para menor
        resultado.sort(key=lambda x: x['votos'], reverse=True)

        return {
            "total_votos": total_votos,
            "chapas": resultado
        }

    def associar_chapas_eleicao(self, eleicao_id, chapas_nomes):
        """Associa chapas a uma eleição na tabela EleicaoChapa"""
        try:
            for chapa_nome in chapas_nomes:
                # Buscar o ID da chapa pelo nome
                chapa_data = self.buscar_chapa_por_nome(chapa_nome)
                if chapa_data:
                    chapa_id = chapa_data[0][0]  # Primeiro campo é o ID
                    
                    # Inserir na tabela EleicaoChapa se não existir
                    sql = f"""
                    INSERT OR IGNORE INTO EleicaoChapa (eleicao_id, chapa_id) 
                    VALUES ({eleicao_id}, {chapa_id})
                    """
                    Model().insert(sql)
            print("Chapas associadas à eleição com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao associar chapas à eleição: {e}")
            return False

    def remover_chapas_eleicao(self, eleicao_id):
        """Remove todas as associações de chapas de uma eleição"""
        try:
            sql = f"DELETE FROM EleicaoChapa WHERE eleicao_id = {eleicao_id}"
            Model().delete(sql)
            print("Associações de chapas removidas com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover associações de chapas: {e}")
            return False

    def buscar_chapa_por_nome(self, nome):
        """Busca uma chapa pelo nome"""
        try:
            sql = f"SELECT * FROM Chapa WHERE nome = '{nome}'"
            return Model().get(sql)
        except Exception as e:
            print(f"Erro ao buscar chapa: {e}")
            return None

    def listar_chapas_por_eleicao(self, eleicao_id):
        """Lista as chapas associadas a uma eleição específica"""
        try:
            sql = f"""
            SELECT c.id, c.nome, c.slogan, c.logo, c.numero
            FROM Chapa c
            JOIN EleicaoChapa ec ON c.id = ec.chapa_id
            WHERE ec.eleicao_id = {eleicao_id}
            """
            return Model().get(sql)
        except Exception as e:
            print(f"Erro ao listar chapas da eleição: {e}")
            return []