import re
from enum import Enum



class Consulta():
    def __init__(self,select = "",descricao = "", comando = ""):
        self.select = select
        self.descricao = descricao
        self.comando = comando


class Menu(Enum):
    OP1 = Consulta()
    OP2 = Consulta()
    OP3 = Consulta()
    OP4 = Consulta()
    OP5 = Consulta()
    OP6 = Consulta()
    OP7 = Consulta()
    OP8 = Consulta()
    OP9 = Consulta()
    OP10 = Consulta()
    OP11 = Consulta()
    OP12 = Consulta()
    OP13 = Consulta()
    OP14 = Consulta()
    OP15 = Consulta()

    @classmethod
    def get_opcao(cls,num):
        return cls[f"OP{num}"]



#descreve as consultas uma a uma.


Menu.OP1.value.select = "SELECT IdLoja, IdCarro, AnoFab, ValorDiaria, TipoCombustivel, Placa, Opcionais"
Menu.OP1.value.descricao = "Carros disponíveis por loja e categoria"
Menu.OP1.value.comando = f'''SELECT IdLoja, IdCarro, AnoFab, ValorDiaria, TipoCombustivel, Placa, Opcionais
    FROM CARROS1 NATURAL JOIN Lojas
    WHERE  IdCarro NOT IN (SELECT IdCarro FROM Locacoes WHERE DataFinal IS NULL)
    GROUP BY IdLoja,NomeCat,IdCarro,AnoFab, ValorDiaria, TipoCombustivel, Placa, Opcionais
    ORDER BY IdLoja;
'''

Menu.OP2.value.select = "SELECT Carros1.IdCarro, Placa, COUNT(CARROS1.IdCarro) as QtdManutencoes"
Menu.OP2.value.descricao = "Frequência que cada carro sofre manutenção"
Menu.OP2.value.comando = f'''SELECT Carros1.IdCarro, Placa, COUNT(CARROS1.IdCarro) as QtdManutencoes
from Carros1 join Manutencoes on Carros1.IdCarro = Manutencoes.IdCarro
group by Carros1.IdCarro,Placa;
'''

Menu.OP3.value.select = 'SELECT NomeCat, COUNT(NomeCat) as "Qtd Manutencoes"'
Menu.OP3.value.descricao = "Frequência que cada modelo decarro sofre manutenção"
Menu.OP3.value.comando = f'''SELECT NomeCat, COUNT(NomeCat) as "Qtd Manutencoes"
from Carros1 join Manutencoes on Carros1.IdCarro = Manutencoes.IdCarro
group by NomeCat;
'''

Menu.OP4.value.select = "SELECT idFuncionario, Nome, IdLocacao, Carros1.IdCarro,NomeCat,Chassi,AnoFab,ValorDiaria,TipoCombustivel,Placa"
Menu.OP4.value.descricao = "Carros locados por funcionário"
Menu.OP4.value.comando = f'''SELECT idFuncionario, Nome, IdLocacao, Carros1.IdCarro,NomeCat,Chassi,AnoFab,ValorDiaria,TipoCombustivel,Placa
    FROM FUNCIONARIOS NATURAL JOIN LOCACOES JOIN CARROS1 ON CARROS1.IdCarro = Locacoes.idCarro
    ORDER BY IdFuncionario,NomeCat;
'''

Menu.OP5.value.select = "select round(avg(ValorDiaria),2) as Valor_diaria_medio"
Menu.OP5.value.descricao = "Valores médios de diária"
Menu.OP5.value.comando = f'''select round(avg(ValorDiaria),2) as Valor_diaria_medio
from carros1 join locacoes on carros1.idCarro = locacoes.Idcarro
'''

Menu.OP6.value.select = "select sum(Duracao)/count(*) as Duracao_Media"
Menu.OP6.value.descricao = "Valores médios de tempo de locação"
Menu.OP6.value.comando = f'''select sum(Duracao)/count(*) as Duracao_Media from
(select (coalesce(datafinal,now()) - datainicio) as Duracao
from carros1 join locacoes on carros1.idCarro = locacoes.Idcarro
group by datafinal,datainicio) as DuracaoLocacao;
'''

Menu.OP7.value.select = "SELECT IdLocatario, Nome, Email, Telefone, CARROS1.IdCarro, NomeCat, Placa, ValorDiaria, DataInicio, DataDevPrevista"
Menu.OP7.value.descricao = "carros em locação  e seus clientes"
Menu.OP7.value.comando = f'''SELECT IdLocatario, Nome, Email, Telefone, CARROS1.IdCarro, NomeCat, Placa, ValorDiaria, DataInicio, DataDevPrevista
    FROM LOCATARIOS NATURAL JOIN LOCACOES JOIN CARROS1 ON CARROS1.IdCarro = Locacoes.idCarro
    WHERE DataFinal IS NULL;
'''

Menu.OP8.value.select = "SELECT DISTINCT Nome, Email, Telefone"
Menu.OP8.value.descricao = "Clientes atendidos por gerentes ou mecanicos"
Menu.OP8.value.comando = f'''SELECT DISTINCT Nome, Email, Telefone
        FROM Locatarios
        NATURAL JOIN Locacoes
        LEFT JOIN GERENTES ON Locacoes.IdFuncionario = GERENTES.IdFuncionario
        LEFT JOIN MECANICOS ON Locacoes.IdFuncionario = MECANICOS.IdFuncionario
        WHERE GERENTES.IdFuncionario IS NOT NULL OR MECANICOS.IdFuncionario IS NOT NULL
'''

Menu.OP9.value.select = "select round(avg(custo),2) as custo_medio, max(custo) as conserto_mais_caro"
Menu.OP9.value.descricao = "Custo médio de conserto, consertos mais caros"
Menu.OP9.value.comando = f'''select round(avg(custo),2) as custo_medio, max(custo) as conserto_mais_caro
from carros1 join consertos on carros1.idcarro = consertos.idcarro
'''

Menu.OP10.value.select = "select count(mes || '-' || ano) as qtd,mes,ano from (select date_part('month',data) as mes, date_part('year',data) as ano"
Menu.OP10.value.descricao = "Acionamento de seguros por mês"
Menu.OP10.value.comando = f'''select count(mes || '-' || ano) as qtd,mes,ano from (select date_part('month',data) as mes, date_part('year',data) as ano
from carros1 join acionamentos on carros1.idcarro = acionamentos.idcarro
 group by carros1.idcarro,data) as acionamentos
group by mes,ano;
'''

Menu.OP11.value.select = "select round(avg(custoLocacao),2) as Valor_medio_diaria"
Menu.OP11.value.descricao = "gasto médio e frequência de locação, lojas mais usadas por usuário"
Menu.OP11.value.comando = f'''select round(avg(custoLocacao),2) as Valor_medio_diaria from
(select (extract (EPOCH from (coalesce(datafinal,now()) - datainicio))/(3600*24)*ValorDiaria) as CustoLocacao,valorDiaria,datafinal,datainicio
 from carros1 join locacoes on carros1.idCarro = locacoes.Idcarro
group by datafinal,datainicio,valorDiaria) as CustoLocacao;
'''

Menu.OP12.value.select = "select placa, idLoja,qtd"
Menu.OP12.value.descricao = "carro mais alugado de cada loja"
Menu.OP12.value.comando = f'''select placa, idLoja,qtd from
(select  count(*) as qtd,placa,carros1.idLoja
from locacoes join carros1 on locacoes.idCarro = carros1.idcarro
group by carros1.idLoja,carros1.idCarro,placa) as subconsulta
group by placa,IdLoja,qtd
having qtd = max(qtd)
'''

Menu.OP13.value.select = "select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia"
Menu.OP13.value.descricao = "Quantas vezes cada forma de pagamento foi utilizado"
Menu.OP13.value.comando = f'''select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia from carros1 join locacoes on carros1.idcarro = locacoes.idcarro group by tipopag;
'''

Menu.OP14.value.select = "select greatest(qtd_cartao,qtd_transferencia) as qtd,(qtd_cartao < qtd_transferencia) as tipopag from (select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia"
Menu.OP14.value.descricao = "qual forma de pagamento foi mais utilizada"
Menu.OP14.value.comando = f'''select greatest(qtd_cartao,qtd_transferencia) as qtd,(qtd_cartao < qtd_transferencia) as tipopag from (select count(*) filter (where tipopag = false) as qtd_cartao, count(*) filter (where tipopag = true) as qtd_transferencia
from carros1 join locacoes on carros1.idcarro = locacoes.idcarro
group by tipopag) as tipos
 group by qtd_cartao,qtd_transferencia;
'''

Menu.OP15.value.select = "SELECT IdCarro, PLACA, NomeCat,ValorDiaria"
Menu.OP15.value.descricao = "carros que estão fora da loja"
Menu.OP15.value.comando = f'''SELECT IdCarro, PLACA, NomeCat,ValorDiaria
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
    for item in Menu:
        print(f"{item.name}. {item.value.descricao}")

    opcao = int(input("Escolha a consulta que deseja realizar\n"))
    print(f"\n{opcao=}")
    print(f"{Menu.get_opcao(opcao).value.select} \n\nDentre os valores acima, especifique os que deseja restringir")

def main():
    formatar_consulta(7, "abc=xyz", "a=5", "kj = ast")
    listar_consultas()

if __name__ == "__main__":
    main()
