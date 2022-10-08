import re

listaSelect = [
"SELECT IdLoja, IdCarro, AnoFab, ValorDiaria, TipoCombustivel, Placa, Opcionais",
"SELECT Carros1.IdCarro, Placa, COUNT(CARROS1.IdCarro) as QtdManutencoes",
'SELECT NomeCat, COUNT(NomeCat) as "Qtd Manutencoes"',
"SELECT idFuncionario, Nome, IdLocacao, Carros1.IdCarro,NomeCat,Chassi,AnoFab,ValorDiaria,TipoCombustivel,Placa",
"select round(avg(ValorDiaria),2) as Valor_diaria_medio",
"select sum(Duracao)/count(*) as Duracao_Media",
"SELECT IdLocatario, Nome, Email, Telefone, CARROS1.IdCarro, NomeCat, Placa, ValorDiaria, DataInicio, DataDevPrevista",
"SELECT DISTINCT Nome, Email, Telefone",
"select round(avg(custo),2) as custo_medio, max(custo) as conserto_mais_caro",
"select count(mes || '-' || ano) as qtd,mes,ano from (select date_part('month',data) as mes, date_part('year',data) as ano",
"select round(avg(custoLocacao),2) as Valor_medio_diaria",
"select placa, idLoja,qtd",
"select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia",
"select greatest(qtd_cartao,qtd_transferencia) as qtd,(qtd_cartao < qtd_transferencia) as tipopag from (select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia",
"SELECT IdCarro, PLACA, NomeCat,ValorDiaria"
    ]

#descreve as consultas uma a uma.
listaOpcoesDescricao = [
"Carros disponíveis por loja e categoria",
"Frequência que cada carro sofre manutenção ",
"Frequência que cada modelo decarro sofre manutenção",
"Carros locados por funcionário",
"Valores médios de diária" ,
"Valores médios de tempo de locação",
"carros em locação  e seus clientes",
"Clientes atendidos por gerentes ou mecanicos",
"Custo médio de conserto, consertos mais caros",
"Acionamento de seguros por mês",
"gasto médio e frequência de locação, lojas mais usadas por usuário",
"carro mais alugado de cada loja",
"Quantas vezes cada forma de pagamento foi utilizado",
"qual forma de pagamento foi mais utilizada",
"carros que estão fora da loja",
    ]


#lista de consultas assim como seria enviado ao banco de dados, sem formatação adicional
listaOpcoesRaw = [
f'''SELECT IdLoja, IdCarro, AnoFab, ValorDiaria, TipoCombustivel, Placa, Opcionais
    FROM CARROS1 NATURAL JOIN Lojas
    WHERE  IdCarro NOT IN (SELECT IdCarro FROM Locacoes WHERE DataFinal IS NULL)
    GROUP BY IdLoja,NomeCat,IdCarro,AnoFab, ValorDiaria, TipoCombustivel, Placa, Opcionais
    ORDER BY IdLoja;
''',

f'''SELECT Carros1.IdCarro, Placa, COUNT(CARROS1.IdCarro) as QtdManutencoes
from Carros1 join Manutencoes on Carros1.IdCarro = Manutencoes.IdCarro
group by Carros1.IdCarro,Placa;
''',

f'''SELECT NomeCat, COUNT(NomeCat) as "Qtd Manutencoes"
from Carros1 join Manutencoes on Carros1.IdCarro = Manutencoes.IdCarro
group by NomeCat;
''',

f'''SELECT idFuncionario, Nome, IdLocacao, Carros1.IdCarro,NomeCat,Chassi,AnoFab,ValorDiaria,TipoCombustivel,Placa
    FROM FUNCIONARIOS NATURAL JOIN LOCACOES JOIN CARROS1 ON CARROS1.IdCarro = Locacoes.idCarro
    ORDER BY IdFuncionario,NomeCat;
''',

f'''select round(avg(ValorDiaria),2) as Valor_diaria_medio
from carros1 join locacoes on carros1.idCarro = locacoes.Idcarro
''',

f'''select sum(Duracao)/count(*) as Duracao_Media from
(select (coalesce(datafinal,now()) - datainicio) as Duracao
from carros1 join locacoes on carros1.idCarro = locacoes.Idcarro
group by datafinal,datainicio) as DuracaoLocacao;
''',

f'''SELECT IdLocatario, Nome, Email, Telefone, CARROS1.IdCarro, NomeCat, Placa, ValorDiaria, DataInicio, DataDevPrevista
    FROM LOCATARIOS NATURAL JOIN LOCACOES JOIN CARROS1 ON CARROS1.IdCarro = Locacoes.idCarro
    WHERE DataFinal IS NULL;
''',

f'''SELECT DISTINCT Nome, Email, Telefone
        FROM Locatarios
        NATURAL JOIN Locacoes
        LEFT JOIN GERENTES ON Locacoes.IdFuncionario = GERENTES.IdFuncionario
        LEFT JOIN MECANICOS ON Locacoes.IdFuncionario = MECANICOS.IdFuncionario
        WHERE GERENTES.IdFuncionario IS NOT NULL OR MECANICOS.IdFuncionario IS NOT NULL
''',

f'''select round(avg(custo),2) as custo_medio, max(custo) as conserto_mais_caro
from carros1 join consertos on carros1.idcarro = consertos.idcarro
''',

f'''select count(mes || '-' || ano) as qtd,mes,ano from (select date_part('month',data) as mes, date_part('year',data) as ano
from carros1 join acionamentos on carros1.idcarro = acionamentos.idcarro
 group by carros1.idcarro,data) as acionamentos
group by mes,ano;
''',

f'''select round(avg(custoLocacao),2) as Valor_medio_diaria from
(select (extract (EPOCH from (coalesce(datafinal,now()) - datainicio))/(3600*24)*ValorDiaria) as CustoLocacao,valorDiaria,datafinal,datainicio
 from carros1 join locacoes on carros1.idCarro = locacoes.Idcarro
group by datafinal,datainicio,valorDiaria) as CustoLocacao;
''',

f'''select placa, idLoja,qtd from
(select  count(*) as qtd,placa,carros1.idLoja
from locacoes join carros1 on locacoes.idCarro = carros1.idcarro
group by carros1.idLoja,carros1.idCarro,placa) as subconsulta
group by placa,IdLoja,qtd
having qtd = max(qtd)
''',
f'''select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia from carros1 join locacoes on carros1.idcarro = locacoes.idcarro group by tipopag;
''',
f'''select greatest(qtd_cartao,qtd_transferencia) as qtd,(qtd_cartao < qtd_transferencia) as tipopag from (select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia
from carros1 join locacoes on carros1.idcarro = locacoes.idcarro
group by tipopag) as tipos
 group by qtd_cartao,qtd_transferencia;
''',
f'''SELECT IdCarro, PLACA, NomeCat,ValorDiaria
        FROM CARROS1
        WHERE IdCarro IN (SELECT IdCarros
                          FROM TRANSFERENCIA
                          WHERE DataChegada IS NULL AND IdCARROS NOT IN (SELECT IdCarro
                                                                         FROM Locacoes
                                                                         WHERE IdLoja IS NOT NULL))
              OR IdCarro IN (SELECT IdCarro
                             FROM Locacoes
                             WHERE IdLoja IS NOT NULL AND IdCarro NOT IN (SELECT IdCarros
                                                                          FROM TRANSFERENCIA
                                                                          WHERE DataSaida > DataFinal))
'''
]

def formatar_consulta(opcao, *args):
    #Itera sobre os valores a serem utilizados nas consultas, que estão no formato variavel = valor, separando os dois itens da string
    for item in args:
        if("=" in item):
            item = item.replace(" ","")
            item_tupla = item.split("=")

            if(len(item_tupla) == 2): #proteção caso o parametro recebido seja a = b = c por engano
                variavel,valor = item_tupla
                print(f"{variavel=},{valor=}")

def listar_consultas():
    print("Menu de consultas\n")
    for index,opcao in enumerate(listaOpcoesDescricao):
        print(f"{index}. {opcao}")

    opcao = int(input("Escolha a consulta que deseja realizar\n"))
    print(f"\n{opcao=}")
    print(f"{listaSelect[opcao]} \n\nDentre os valores acima, especifique os que deseja restringir")

def main():
    formatar_consulta(7, "abc=xyz", "a=5", "kj = ast")
    listar_consultas()

if __name__ == "__main__":
    main()
