# -*- coding: utf-8 -*-
"""
Configuração e Sistema de Email para Urna Eletrônica
===================================================

Este arquivo contém as configurações e funcionalidades completas para envio de emails.
Sistema robusto com fallback automático entre yagmail e smtplib nativo.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configurações do email (ATENÇÃO: Use variáveis de ambiente em produção!)
EMAIL_SISTEMA = os.getenv('URNA_EMAIL', 'ufac.urna@gmail.com')
SENHA_EMAIL = os.getenv('URNA_EMAIL_PASSWORD', 'hanm anjk owxc cdjv')  # Use senha de app do Gmail
SMTP_SERVER = os.getenv('URNA_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('URNA_SMTP_PORT', '587'))

def _verificar_yagmail():
    """Verifica se yagmail está disponível"""
    try:
        import yagmail
        return True
    except ImportError:
        return False

def enviar_comprovante_voto(email_destino, eleicao_titulo, data_voto, codigo_verificacao):
    """
    Envia comprovante de voto por email
    
    Args:
        email_destino (str): Email do eleitor
        eleicao_titulo (str): Título da eleição
        data_voto (str): Data e hora do voto
        codigo_verificacao (str): Código de verificação do voto
        
    Returns:
        bool: True se enviado com sucesso, False caso contrário
    """
    
    assunto = f"Comprovante de Voto - {eleicao_titulo}"
    
    conteudo = f"""🗳️ COMPROVANTE DE VOTO ELETRÔNICO

Eleição: {eleicao_titulo}
Data/Hora: {data_voto}
Código de Verificação: {codigo_verificacao}

✅ Seu voto foi registrado com sucesso!

Este comprovante confirma que você participou do processo eleitoral.
O anonimato do seu voto está garantido pelo sistema.

=== IMPORTANTE ===
• Guarde este comprovante para seus registros
• O código de verificação pode ser usado para auditoria
• Seu voto é secreto e não pode ser identificado

=== SISTEMA DE URNA ELETRÔNICA ===
Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

Obrigado por participar do processo democrático!
"""
    
    # Tentar enviar com yagmail primeiro (mais simples)
    if _verificar_yagmail():
        if _enviar_com_yagmail(email_destino, assunto, conteudo):
            return True
    
    # Fallback para smtplib nativo
    return _enviar_com_smtplib(email_destino, assunto, conteudo)

def _enviar_com_yagmail(email_destino, assunto, conteudo):
    """Envia email usando yagmail"""
    try:
        import yagmail
        yag = yagmail.SMTP(EMAIL_SISTEMA, SENHA_EMAIL)
        yag.send(
            to=email_destino,
            subject=assunto,
            contents=conteudo
        )
        print(f"✅ Email enviado via yagmail para: {email_destino}")
        return True
    except Exception as e:
        print(f"❌ Erro com yagmail: {e}")
        return False

def _enviar_com_smtplib(email_destino, assunto, conteudo):
    """Envia email usando smtplib nativo"""
    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SISTEMA
        msg['To'] = email_destino
        msg['Subject'] = assunto
        
        # Adicionar conteúdo
        msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))
        
        # Conectar e enviar
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SISTEMA, SENHA_EMAIL)
            texto = msg.as_string()
            server.sendmail(EMAIL_SISTEMA, email_destino, texto)
        
        print(f"✅ Email enviado via smtplib para: {email_destino}")
        return True
        
    except Exception as e:
        print(f"❌ Erro com smtplib: {e}")
        return False

def configurar_email_sistema():
    """
    Configura o email do sistema para envio de comprovantes.
    
    Esta função deve ser executada UMA VEZ para configurar as credenciais.
    Exemplo de uso:
    
    ```python
    from config_email import configurar_email_sistema
    configurar_email_sistema()
    ```
    """
    try:
        if _verificar_yagmail():
            import yagmail
            # Registrar credenciais no yagmail
            yagmail.register(EMAIL_SISTEMA, SENHA_EMAIL)
            print(f"✅ Email configurado: {EMAIL_SISTEMA}")
        else:
            print(f"⚠️ Yagmail não disponível, usando smtplib nativo")
            print(f"✅ Email configurado: {EMAIL_SISTEMA}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar email: {e}")
        return False

def testar_envio_email(email_teste="teste@exemplo.com"):
    """
    Testa o envio de email.
    
    Args:
        email_teste (str): Email para teste
        
    Returns:
        bool: True se teste passou, False caso contrário
    """
    print(f"🧪 Testando envio de email para: {email_teste}")
    
    if _verificar_yagmail():
        print("📧 Testando com yagmail...")
        if _testar_yagmail(email_teste):
            return True
    
    print("📧 Testando com smtplib...")
    return _testar_smtplib(email_teste)

def _testar_yagmail(email_teste):
    """Testa envio com yagmail"""
    try:
        import yagmail
        yag = yagmail.SMTP(EMAIL_SISTEMA, SENHA_EMAIL)
        yag.send(
            to=email_teste,
            subject="Teste - Sistema de Urna Eletrônica (yagmail)",
            contents="Este é um teste do sistema de email usando yagmail.\n\nSe você recebeu esta mensagem, o sistema está funcionando!"
        )
        print("✅ Teste com yagmail: SUCESSO")
        return True
    except Exception as e:
        print(f"❌ Teste com yagmail: FALHA - {e}")
        return False

def _testar_smtplib(email_teste):
    """Testa envio com smtplib"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SISTEMA
        msg['To'] = email_teste
        msg['Subject'] = "Teste - Sistema de Urna Eletrônica (smtplib)"
        
        conteudo = "Este é um teste do sistema de email usando smtplib nativo.\n\nSe você recebeu esta mensagem, o sistema está funcionando!"
        msg.attach(MIMEText(conteudo, 'plain', 'utf-8'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SISTEMA, SENHA_EMAIL)
            texto = msg.as_string()
            server.sendmail(EMAIL_SISTEMA, email_teste, texto)
        
        print("✅ Teste com smtplib: SUCESSO")
        return True
        
    except Exception as e:
        print(f"❌ Teste com smtplib: FALHA - {e}")
        return False

def obter_configuracao_email():
    """
    Retorna as configurações atuais de email.
    
    Returns:
        dict: Dicionário com as configurações
    """
    return {
        'email_sistema': EMAIL_SISTEMA,
        'smtp_server': SMTP_SERVER,
        'smtp_port': SMTP_PORT,
        'yagmail_disponivel': _verificar_yagmail(),
        'configurado': bool(EMAIL_SISTEMA and SENHA_EMAIL)
    }

# Instruções de configuração
INSTRUCOES_CONFIGURACAO = """
=== CONFIGURAÇÃO DO EMAIL PARA URNA ELETRÔNICA ===

1. CONFIGURAÇÃO COM GMAIL:
   - Acesse sua conta Google
   - Ative a verificação em 2 etapas
   - Gere uma "senha de app" específica
   - Use essa senha, não sua senha normal

2. CONFIGURAR VARIÁVEIS DE AMBIENTE:
   
   Linux/Mac:
   export URNA_EMAIL='sistema@gmail.com'
   export URNA_EMAIL_PASSWORD='sua_senha_de_app'
   
   Windows:
   set URNA_EMAIL=sistema@gmail.com
   set URNA_EMAIL_PASSWORD=sua_senha_de_app

3. EXECUTAR CONFIGURAÇÃO:
   
   python3 -c "from config_email import configurar_email_sistema; configurar_email_sistema()"

4. TESTAR ENVIO:
   
   python3 -c "from config_email import testar_envio_email; testar_envio_email('seu_email@teste.com')"

=== SEGURANÇA ===
- NUNCA coloque senhas diretamente no código
- Use sempre variáveis de ambiente
- Use senhas de app, não senhas pessoais
- Em produção, considere usar serviços como SendGrid, AWS SES, etc.

=== TROUBLESHOOTING ===
- "Application-specific password required": Configure senha de app no Gmail
- "Less secure app access": Use senha de app em vez da configuração antiga
- "Authentication failed": Verifique email e senha
- "SMTP connection error": Verifique conexão de internet e firewall
"""

if __name__ == "__main__":
    print(INSTRUCOES_CONFIGURACAO)
    
    print("\n=== STATUS ATUAL ===")
    config = obter_configuracao_email()
    print(f"Email do sistema: {config['email_sistema']}")
    print(f"SMTP Server: {config['smtp_server']}:{config['smtp_port']}")
    print(f"Configurado: {'✅' if config['configurado'] else '❌'}")
    
    if not config['configurado']:
        print("\n⚠️  Configure as variáveis de ambiente antes de usar!")