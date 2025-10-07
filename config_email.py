# -*- coding: utf-8 -*-
"""
Configuração de Email para Urna Eletrônica
=========================================

Este arquivo contém as configurações para envio de comprovantes de votação por email.
"""

import yagmail
import os

# Configurações do email (ATENÇÃO: Use variáveis de ambiente em produção!)
EMAIL_SISTEMA = os.getenv('URNA_EMAIL', 'ufac.urna@gmail.com')
SENHA_EMAIL = os.getenv('URNA_EMAIL_PASSWORD', 'hanm anjk owxc cdjv')  # Use senha de app do Gmail
SMTP_SERVER = os.getenv('URNA_SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('URNA_SMTP_PORT', '587'))

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
        # Registrar credenciais no yagmail
        yagmail.register(EMAIL_SISTEMA, SENHA_EMAIL)
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
    """
    try:
        yag = yagmail.SMTP(EMAIL_SISTEMA)
        
        yag.send(
            to=email_teste,
            subject="Teste - Sistema de Urna Eletrônica",
            contents="""Este é um email de teste do sistema de urna eletrônica.
            
Se você recebeu esta mensagem, o sistema de email está funcionando corretamente.

Urna Eletrônica - Sistema Eleitoral
"""
        )
        
        print(f"✅ Email de teste enviado para: {email_teste}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de email: {e}")
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