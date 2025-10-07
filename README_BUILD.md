## Pré-requisitos:
```bash
pip install pyinstaller pillow ttkbootstrap yagmail
```

## Comando para Gerar Linux:
```bash
cd /caminho/para/projeto
python -m PyInstaller --onefile --windowed \
  --name UrnaEletronica_Linux \
  --add-data "app/src/*:src" \
  --add-data "db:." \
  --add-data "config_email.py:." \
  --paths="app" \
  --paths="app/view" \
  --paths="app/control" \
  --paths="app/model" \
  --paths="app/conexao" \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=model.model \
  --hidden-import=conexao.conexao \
  --hidden-import=yagmail \
  --hidden-import=smtplib \
  --hidden-import=email.mime.text \
  --hidden-import=email.mime.multipart \
  app/view/view.py

  ou

  python -m PyInstaller --onefile --windowed --name UrnaEletronica_Linux --add-data "db.db:." --add-data "config_email.py:." --add-data "app/src/*:src" --paths="app" --paths="app/view" --paths="app/control" --paths="app/model" --paths="app/conexao" --hidden-import=PIL._tkinter_finder --hidden-import=model.model --hidden-import=conexao.conexao --hidden-import=yagmail --hidden-import=smtplib --hidden-import=email.mime.text --hidden-import=email.mime.multipart app/view/view.py
```

## Comando para Gerar Windows:
```cmd
cd C:\caminho\para\projeto
python -m PyInstaller --onefile --windowed ^
  --name UrnaEletronica_Windows.exe ^
  --add-data "app/src/*;src" ^
  --add-data "db.db;." ^
  --add-data "config_email.py;." ^
  --paths="app" ^
  --paths="app/view" ^
  --paths="app/control" ^
  --paths="app/model" ^
  --paths="app/conexao" ^
  --hidden-import=PIL._tkinter_finder ^
  --hidden-import=model.model ^
  --hidden-import=conexao.conexao ^
  --hidden-import=yagmail ^
  --hidden-import=smtplib ^
  --hidden-import=email.mime.text ^
  --hidden-import=email.mime.multipart ^
  app/view/view.py

  ou

  python -m PyInstaller --onefile --windowed --name UrnaEletronica_Windows.exe --add-data "app/src/*;src" --add-data "db.db;." --add-data "config_email.py;." --paths="app" --paths="app/view" --paths="app/control" --paths="app/model" --paths="app/conexao" --hidden-import=PIL._tkinter_finder --hidden-import=model.model --hidden-import=conexao.conexao --hidden-import=yagmail --hidden-import=smtplib --hidden-import=email.mime.text --hidden-import=email.mime.multipart app/view/view.py
```

## Resultado
O executável estará em `dist/UrnaEletronica_Linux` ou `dist/UrnaEletronica_Windows.exe`

## ⚡ Teste Rápido

### Desenvolvimento:
```bash
# Deve funcionar sem erros
python app/view/view.py
```

### Executável:
```bash
# Copiar para qualquer pasta e testar
cp dist/UrnaEletronica_Linux /tmp/
cd /tmp
chmod +x UrnaEletronica_Linux
./UrnaEletronica_Linux
```

### Dados Iniciais do Executável:
**IMPORTANTE:** Na primeira execução, o executável criará um banco vazio em `~/.urna_eletronica/db.db`. Para usar com dados de desenvolvimento:

```bash
# Copiar banco de desenvolvimento para pasta persistente
cp db.db ~/.urna_eletronica/db.db
```

**Usuários padrão (se usando banco de desenvolvimento):**
- **Usuário:** root | **Senha:** root
- **Usuário:** Limeira | **Senha:** tesi25

## 🔧 Resolução de Problemas

### "Permission denied"
```bash
chmod +x UrnaEletronica_Linux
```

## Como Usar o Executável Baixado:

### Para Usuários Linux:
```bash
# 1. Dar permissão de execução
chmod +x UrnaEletronica_Linux

# 2. Executar
./UrnaEletronica_Linux
```

### Para usuários Windows:
```cmd
# executar (duplo-clique ou pelo cmd) ~mto mais facil af~
UrnaEletronica_Windows.exe
```