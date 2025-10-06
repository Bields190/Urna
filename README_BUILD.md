## Pré-requisitos:
```bash
pip install pyinstaller pillow ttkbootstrap
```

## Comando para Gerar Linux:
```bash
cd /caminho/para/projeto
python -m PyInstaller --onefile --windowed \
  --name UrnaEletronica_Linux \
  --add-data "app/src/*:src" \
  --add-data "db:." \
  --paths="app" \
  --paths="app/view" \
  --paths="app/control" \
  --paths="app/model" \
  --paths="app/conexao" \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=model.model \
  --hidden-import=conexao.conexao \
  app/view/view.py
```

## Comando para Gerar Windows:
```cmd
cd C:\caminho\para\projeto
python -m PyInstaller --onefile --windowed ^
  --name UrnaEletronica_Windows.exe ^
  --add-data "app/src/*;src" ^
  --add-data "db;." ^
  --paths="app" ^
  --paths="app/view" ^
  --paths="app/control" ^
  --paths="app/model" ^
  --paths="app/conexao" ^
  --hidden-import=PIL._tkinter_finder ^
  --hidden-import=model.model ^
  --hidden-import=conexao.conexao ^
  app/view/view.py
```

## GitHub Actions (Automático)
O projeto inclui workflow que gera automaticamente executáveis para Linux e Windows quando você criar uma tag/release.

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