# Como Gerar o Executável

## Pré-requisitos:
```bash
pip install pyinstaller
```

## Comando para Gerar (linux only):
```bash
cd /caminho/para/projeto
python -m PyInstaller --onefile --windowed \
  --name UrnaEletronica \
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

## Resultado do ~.exe~
teoricamente ficará em `dist/UrnaEletronica`