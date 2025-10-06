# Como Gerar o Executável

## Pré-requisitos:
```bash
pip install pyinstaller
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
O executável estará em `dist/UrnaEletronica`

## Como Usar o Executável Baixado:

### Para Usuários Linux:
```bash
# 1. Dar permissão de execução
chmod +x UrnaEletronica_v1

# 2. Executar
./UrnaEletronica_v1
```
ou clicar nele

### Para usuários Windows:
```cmd
# executar (duplo-clique ou pelo cmd)
UrnaEletronica_Windows.exe
```

### Requisitos do Sistema:

**Linux:**
- Linux 64-bit
- Interface gráfica (X11/Wayland)
- Bibliotecas básicas do sistema (geralmente já instaladas)

**Windows:**
- Windows 7/8/10/11 (64-bit)
- Interface gráfica