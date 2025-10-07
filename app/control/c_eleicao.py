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
        
    def obter_status_eleicao(self, data_inicio, data_fim, status_bd=None):
        """Determina o status da eleição baseado nas datas e status do banco"""
        # Se o status do banco for 0 (encerrada manualmente), sempre retornar "Encerrada"
        if status_bd is not None and status_bd == 0:
            return "Encerrada"
            
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
            _, _, data_inicio, data_fim, status_bd = eleicao_data[0]  # Incluindo status
            status = self.obter_status_eleicao(data_inicio, data_fim, status_bd)
            return status == "Ativa"
        return False

    def pode_editar_eleicao(self, id):
        """Verifica se uma eleição pode ser editada (apenas agendadas)"""
        eleicao_data = self.buscar_eleicao(id)
        if eleicao_data:
            _, _, data_inicio, data_fim, status_bd = eleicao_data[0]  # Incluindo status
            status = self.obter_status_eleicao(data_inicio, data_fim, status_bd)
            return status == "Agendada"
        return False

    def pode_deletar_eleicao(self, id):
        """Verifica se uma eleição pode ser deletada (apenas agendadas)"""
        return self.pode_editar_eleicao(id)

    def encerrar_eleicao(self, id):
        """Encerra uma eleição ativa alterando sua data de fim para hoje, status para encerrada e calcula resultados"""        
        if not self.validar_eleicao_ativa(id):
            print("Apenas eleições ativas podem ser encerradas!")
            return False
            
        eleicao_data = self.buscar_eleicao(id)
        if eleicao_data:
            id_el, titulo, data_inicio, _, _ = eleicao_data[0]  # Incluindo status
            hoje = datetime.now().strftime('%Y-%m-%d')
            
            try:
                # 1. Atualizar eleição com data de fim sendo hoje e status como encerrada
                sql_update = f"""
                UPDATE Eleicao 
                SET data_fim = '{hoje}', status = 0 
                WHERE id = {id_el}
                """
                result = Model().update(sql_update)
                if not result:
                    print("Erro ao encerrar eleição.")
                    return False
                
                # 2. Calcular e salvar resultados no banco
                print("Calculando resultados da eleição...")
                sucesso_calculo = self._calcular_e_salvar_resultados(id_el)
                
                if sucesso_calculo:
                    print("Eleição encerrada e resultados calculados com sucesso!")
                    return True
                else:
                    print("Eleição encerrada, mas houve erro no cálculo dos resultados.")
                    return False
                    
            except Exception as e:
                print(f"Erro ao associar chapas: {e}")
            return False
    
    def arquivar_eleicao(self, id):
        """Arquiva uma eleição (não aparece na tela normal)"""
        try:
            sql = f"UPDATE Eleicao SET arquivada = 1 WHERE id = {id}"
            resultado = Model().update(sql)
            if resultado:
                print("Eleição arquivada com sucesso!")
                return True
            else:
                print("Erro ao arquivar eleição.")
                return False
        except Exception as e:
            print(f"Erro ao arquivar eleição: {e}")
            return False
    
    def desarquivar_eleicao(self, id):
        """Desarquiva uma eleição (volta a aparecer na tela normal)"""
        try:
            sql = f"UPDATE Eleicao SET arquivada = 0 WHERE id = {id}"
            resultado = Model().update(sql)
            if resultado:
                print("Eleição desarquivada com sucesso!")
                return True
            else:
                print("Erro ao desarquivar eleição.")
                return False
        except Exception as e:
            print(f"Erro ao desarquivar eleição: {e}")
            return False
    
    def listar_eleicoes_filtradas(self, filtro="todas"):
        """Lista eleições com filtro aplicado
        
        Args:
            filtro (str): 'todas', 'agendadas', 'ativas', 'finalizadas', 'arquivadas'
        
        Returns:
            list: Lista de eleições filtradas
        """
        from datetime import datetime
        hoje = datetime.now().strftime('%Y-%m-%d')
        
        if filtro == "todas":
            # Todas exceto arquivadas
            sql = f"""
            SELECT id, titulo, data_inicio, data_fim, status 
            FROM Eleicao 
            WHERE arquivada = 0
            ORDER BY data_inicio DESC
            """
        
        elif filtro == "agendadas":
            # Eleições que ainda não começaram
            sql = f"""
            SELECT id, titulo, data_inicio, data_fim, status 
            FROM Eleicao 
            WHERE status = 1 AND data_inicio > '{hoje}' AND arquivada = 0
            ORDER BY data_inicio ASC
            """
        
        elif filtro == "ativas":
            # Eleições em andamento
            sql = f"""
            SELECT id, titulo, data_inicio, data_fim, status 
            FROM Eleicao 
            WHERE status = 1 AND data_inicio <= '{hoje}' AND data_fim >= '{hoje}' AND arquivada = 0
            ORDER BY data_inicio ASC
            """
        
        elif filtro == "finalizadas":
            # Eleições encerradas
            sql = f"""
            SELECT id, titulo, data_inicio, data_fim, status 
            FROM Eleicao 
            WHERE status = 0 AND arquivada = 0
            ORDER BY data_fim DESC
            """
        
        elif filtro == "arquivadas":
            # Eleições arquivadas
            sql = f"""
            SELECT id, titulo, data_inicio, data_fim, status 
            FROM Eleicao 
            WHERE arquivada = 1
            ORDER BY data_inicio DESC
            """
        
        else:
            # Fallback para 'todas'
            return self.listar_eleicoes_filtradas("todas")
        
        try:
            resultado = Model().get(sql)
            return resultado if resultado else []
        except Exception as e:
            print(f"Erro ao listar eleições filtradas: {e}")
            return []
    
    def obter_estatisticas_filtros(self):
        """Retorna contadores para cada filtro"""
        try:
            from datetime import datetime
            hoje = datetime.now().strftime('%Y-%m-%d')
            
            # Contar cada categoria
            contadores = {}
            
            # Todas (exceto arquivadas)
            sql_todas = "SELECT COUNT(*) FROM Eleicao WHERE arquivada = 0"
            contadores['todas'] = Model().get(sql_todas)[0][0]
            
            # Agendadas
            sql_agendadas = f"SELECT COUNT(*) FROM Eleicao WHERE status = 1 AND data_inicio > '{hoje}' AND arquivada = 0"
            contadores['agendadas'] = Model().get(sql_agendadas)[0][0]
            
            # Ativas
            sql_ativas = f"SELECT COUNT(*) FROM Eleicao WHERE status = 1 AND data_inicio <= '{hoje}' AND data_fim >= '{hoje}' AND arquivada = 0"
            contadores['ativas'] = Model().get(sql_ativas)[0][0]
            
            # Finalizadas
            sql_finalizadas = f"SELECT COUNT(*) FROM Eleicao WHERE status = 0 AND arquivada = 0"
            contadores['finalizadas'] = Model().get(sql_finalizadas)[0][0]
            
            # Arquivadas
            sql_arquivadas = "SELECT COUNT(*) FROM Eleicao WHERE arquivada = 1"
            contadores['arquivadas'] = Model().get(sql_arquivadas)[0][0]
            
            return contadores
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {'todas': 0, 'agendadas': 0, 'ativas': 0, 'finalizadas': 0, 'arquivadas': 0}

    def _calcular_e_salvar_resultados(self, eleicao_id):
        """Calcula os resultados da eleição e salva na tabela Resultado"""
        try:
            # Limpar resultados anteriores para esta eleição (se existirem)
            sql_delete = f"DELETE FROM Resultado WHERE eleicao_id = {eleicao_id}"
            Model().delete(sql_delete)
            
            # Buscar todas as chapas da eleição
            chapas = m_chapa.Chapa.listar_por_eleicao(eleicao_id)
            
            if not chapas:
                print("Nenhuma chapa encontrada para esta eleição.")
                return True  # Não é erro, apenas não há chapas
            
            # Calcular votos para cada chapa
            resultados_calculados = []
            total_votos_eleicao = 0
            
            for chapa in chapas:
                chapa_id, nome, slogan, logo = chapa
                votos = m_voto.Voto.contar_por_chapa(chapa_id, eleicao_id)
                total_votos_eleicao += votos
                
                resultados_calculados.append({
                    'chapa_id': chapa_id,
                    'nome': nome,
                    'votos': votos
                })
            
            # Salvar resultados na tabela Resultado
            for resultado in resultados_calculados:
                sql_insert = f"""
                INSERT INTO Resultado (eleicao_id, chapa_id, total_votos) 
                VALUES ({eleicao_id}, {resultado['chapa_id']}, {resultado['votos']})
                """
                Model().insert(sql_insert)
            
            print(f"Resultados salvos: {len(resultados_calculados)} chapas, {total_votos_eleicao} votos totais")
            return True
            
        except Exception as e:
            print(f"Erro ao calcular e salvar resultados: {e}")
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
            # Verificar se a eleição tem 4, 5 ou 6 campos
            if len(eleicao) >= 5:
                # Formato: (id, titulo, data_inicio, data_fim, status_bd, ...)
                _, _, data_inicio, data_fim, status_bd = eleicao[:5]
                status = self.obter_status_eleicao(data_inicio, data_fim, status_bd)
            elif len(eleicao) == 4:
                _, _, data_inicio, data_fim = eleicao
                status = self.obter_status_eleicao(data_inicio, data_fim)
            else:
                continue  # Pular eleições com formato inválido
            
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
        
        Prioriza dados pré-calculados da tabela Resultado, se não existir calcula em tempo real.
        """
        # Primeiro, tentar buscar resultados pré-calculados
        resultados_salvos = self._buscar_resultados_salvos(eleicao_id)
        
        if resultados_salvos:
            print("Usando resultados pré-calculados do banco")
            return resultados_salvos
        
        # Se não há resultados salvos, calcular em tempo real
        print("Calculando resultados em tempo real")
        return self._calcular_resultados_tempo_real(eleicao_id)
    
    def _buscar_resultados_salvos(self, eleicao_id):
        """Busca resultados pré-calculados da tabela Resultado"""
        try:
            sql = f"""
            SELECT r.chapa_id, c.nome, c.slogan, c.logo, r.total_votos
            FROM Resultado r
            JOIN Chapa c ON r.chapa_id = c.id
            WHERE r.eleicao_id = {eleicao_id}
            ORDER BY r.total_votos DESC
            """
            
            resultados_db = Model().get(sql)  # Usar 'get' em vez de 'select'
            
            if not resultados_db:
                return None
            
            total_votos = sum(row[4] for row in resultados_db)
            resultado = []
            
            for row in resultados_db:
                chapa_id, nome, slogan, logo, votos = row
                percentual = (votos / total_votos * 100) if total_votos > 0 else 0
                
                resultado.append({
                    "chapa_id": chapa_id,
                    "nome": nome,
                    "slogan": slogan,
                    "logo": logo,
                    "votos": votos,
                    "percentual": round(percentual, 2)
                })
            
            return {
                "total_votos": total_votos,
                "chapas": resultado
            }
            
        except Exception as e:
            print(f"Erro ao buscar resultados salvos: {e}")
            return None
    
    def _calcular_resultados_tempo_real(self, eleicao_id):
        """Calcula resultados em tempo real (método original)"""
        chapas = m_chapa.Chapa.listar_por_eleicao(eleicao_id)
        total_votos = m_voto.Voto.contar_total_eleicao(eleicao_id)
        resultado = []

        for chapa in chapas:
            chapa_id, nome, slogan, logo = chapa
            votos = m_voto.Voto.contar_por_chapa(chapa_id, eleicao_id)
            percentual = (votos / total_votos * 100) if total_votos > 0 else 0
            resultado.append({
                "chapa_id": chapa_id,
                "nome": nome,
                "slogan": slogan,
                "logo": logo,
                "votos": votos,
                "percentual": round(percentual, 2)  # arredonda p/ 2 casas decimais
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
                # Se a chapa vem no formato "ID - Nome", extrair apenas o nome
                if ' - ' in chapa_nome:
                    # Formato: "1 - Core 2 Quad" -> "Core 2 Quad"
                    nome_limpo = chapa_nome.split(' - ', 1)[1]
                else:
                    nome_limpo = chapa_nome
                
                # Buscar o ID da chapa pelo nome
                chapa_data = self.buscar_chapa_por_nome(nome_limpo)
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
            sql = f"SELECT * FROM chapa WHERE nome = '{nome}'"
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