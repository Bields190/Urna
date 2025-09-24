a, b, c = map(int, input("Insira três valores separados por espaço: ").split())

print(f'Valores: A={a}, \nB={b}, \nC={c}')

if a>b and a>c:
    print(f'Maior valor: {a}')
elif b>a and b>c:
    print(f'Maior valor: {b}')
else:
    print(f'Maior valor: {c}')
