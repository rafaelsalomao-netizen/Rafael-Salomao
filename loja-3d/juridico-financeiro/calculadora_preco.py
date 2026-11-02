#!/usr/bin/env python3
"""Calculadora de preço mínimo para peças impressas em 3D.

Uso:
    python3 calculadora_preco.py GRAMAS HORAS_IMPRESSAO MINUTOS_TRABALHO [--canal ml|site]

Exemplo (árvore de nomes, 200 g, 9 h de impressão, 40 min de trabalho manual):
    python3 calculadora_preco.py 200 9 40 --canal ml

Edite a seção PARAMETROS com os seus números reais.
"""
import sys

# ---------------- PARAMETROS (edite) ----------------
PRECO_FILAMENTO_KG = 110.0   # R$ por kg de PLA (média das marcas nacionais)
CUSTO_ENERGIA_KWH  = 0.95    # R$ por kWh na sua conta
CONSUMO_IMPRESSORA = 0.10    # kW médios da Bambu A1 imprimindo PLA
VALOR_IMPRESSORA   = 2800.0  # R$ pagos na máquina
VIDA_UTIL_HORAS    = 3000.0  # horas até trocar/revisar (mesa, bico, extrusora)
MANUTENCAO_POR_H   = 0.40    # R$ por hora (bicos, placa, lubrificante, fita)
TAXA_FALHA         = 0.10    # 10% das impressões dão errado: entra no custo
VALOR_HORA_TRABALHO= 35.0    # R$ pela sua hora (preparar, trocar cor, lixar, embalar, atender)
EMBALAGEM          = 4.50    # caixa + papel + adesivo + cartão
MARGEM_LUCRO       = 0.40    # 40% sobre o custo total (lucro real da loja)
# taxas por canal: (percentual, custo fixo por unidade, frete que você paga)
CANAIS = {
    "site": (0.0399, 0.0, 0.0),    # Pix/link Mercado Pago ~4%; frete pago pelo cliente
    "ml":   (0.17,   0.0, 22.0),   # Premium ~17% + frete grátis obrigatório (>= R$79). Confira no simulador!
    "ml79": (0.13,   6.5, 0.0),    # Clássico ~13% + custo fixo p/ item abaixo de R$79; frete pago pelo cliente
}
# ----------------------------------------------------

def custo(gramas, horas, minutos_trabalho):
    material   = gramas / 1000 * PRECO_FILAMENTO_KG
    energia    = horas * CONSUMO_IMPRESSORA * CUSTO_ENERGIA_KWH
    maquina    = horas * (VALOR_IMPRESSORA / VIDA_UTIL_HORAS + MANUTENCAO_POR_H)
    producao   = (material + energia + maquina) * (1 + TAXA_FALHA)
    trabalho   = minutos_trabalho / 60 * VALOR_HORA_TRABALHO
    return {
        "material": material, "energia": energia, "maquina": maquina,
        "falhas": producao - (material + energia + maquina),
        "trabalho": trabalho, "embalagem": EMBALAGEM,
        "total": producao + trabalho + EMBALAGEM,
    }

def preco(custo_total, canal):
    pct, fixo, frete = CANAIS[canal]
    base = custo_total * (1 + MARGEM_LUCRO) + fixo + frete
    return base / (1 - pct)       # a comissão incide sobre o preço final

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    canal = "site"
    if "--canal" in sys.argv:
        canal = sys.argv[sys.argv.index("--canal") + 1]
    if len(args) < 3:
        print(__doc__); sys.exit(1)
    g, h, m = float(args[0]), float(args[1]), float(args[2])
    c = custo(g, h, m)
    print(f"Peça: {g:.0f} g, {h:.1f} h de impressão, {m:.0f} min de trabalho")
    for k in ("material", "energia", "maquina", "falhas", "trabalho", "embalagem"):
        print(f"  {k:10s} R$ {c[k]:7.2f}")
    print(f"  {'CUSTO':10s} R$ {c['total']:7.2f}")
    print()
    for nome in ("site", "ml79", "ml"):
        p = preco(c["total"], nome)
        pct, fixo, frete = CANAIS[nome]
        lucro = p * (1 - pct) - fixo - frete - c["total"]
        print(f"  canal {nome:5s} preço mínimo R$ {p:7.2f}  (lucro R$ {lucro:6.2f}, R$ {lucro/max(h,0.1):6.2f}/h de impressora)")
    print("\nArredonde para cima (R$ 149, R$ 49,90). Preço de mercado acima do mínimo é lucro; abaixo, não venda.")

if __name__ == "__main__":
    main()
