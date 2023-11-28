import datetime
import TemporaryData
import mysql.connector
import requests
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard

token = ""

session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", token)
session.cookies.set("__Secure-1PSIDTS", "")
session.cookies.set("__Secure-1PSIDCC", "")

bard = Bard(token=token, session=session)

conexao = mysql.connector.connect(host='localhost', user='root', password='', database='bdbot')
cursor = conexao.cursor()


def handle_responses(message) -> str:
    p_message = message.lower()

    if p_message == '$hello':
        return ('Olá, eu sou o Tudy 🤓, o BOT de Estudos!!\n'
                'Essas são as minhas funções principais:'
                '\n1 - Digite: "$Timer" para acessar a aba do Crômetro'
                '\n2 - Digite: "$ContentList" para acessar a aba de Conteúdo de Estudo'
                '\n3 - Digite: "$ToDoList" para acessar a aba de ListaDeTarefas'
                '\n4 - Digite: "$DuvidasIA" para tirar Duvidas com a inteligência Artificial da Google')

    if p_message == "$contentlist":
        if TemporaryData.Counter == 0:
            TemporaryData.Counter = 2
            return (f'Você entrou na aba de Listas de Conteudos 🧠\n\nEscolha uma das seguintes opções:\n\n'
                    f'-> Digite:"$List-in:(Conteudo)" para inserir conteudo na Lista de Conteudos\n'
                    f'-> Digite:"$List-on" para ver os conteudos na Lista de Conteudos\n'
                    f'-> Digite:"$List-out:(IDdoConteudo)" para retirar conteudo da Lista de Conteudos\n'
                    f'-> Digite:"$Sair" para voltar para a Aba de funcionalidades\n')
        else:
            return (f'Você já se encontra em uma Aba, digite "$Sair" para retornar para janela de Abas e após, digite '
                    f'$"ContentList" para entrar na aba de Lista de Conteudos')

    if p_message == "$duvidasia":
        if TemporaryData.Counter == 0:
            TemporaryData.Counter = 4
            return (f'Você entrou na aba de Duvidas com Inteligência Artifical 🤖\n\n'
                    f'-> Digite seu texto começando com o "$" para receber uma resposta da IA integrada\n'
                    f'-> Digite "$Sair" para voltar')
        else:
            return (f'Você já se encontra em uma Aba, digite "$Sair" para retornar para janela de Abas e após, digite '
                    f'"$DuvidasIA" para entrar na aba de Duvidas com Inteligência Artifical 🤖')

    if p_message == "$timer":
        if TemporaryData.Counter == 0:
            TemporaryData.Counter = 3
            return (f'Você entrou na aba do Cronometro ⏲️\n\nEscolha uma das seguintes opções:\n\n'
                    f'-> Digite:"$Start" para iniciar o Cronômetro\n'
                    f'-> Digite:"$Stop" para finalizar o Cronômetro\n'
                    f'-> Digite:"$Pause" para pausar o Cronômetro\n'
                    f'-> Digite:"$ShowAll" para mostrar o Histórico de Estudo\n'
                    f'-> Digite:"$Show:(00/00/0000)" substituindo os zeros pela data para Visualizar o '
                    f'histórico de Estudo da Data em questão'
                    f'-> Digite:"$Sair" para voltar para a Aba de funcionalidades\n')
        else:
            return (f'Você já se encontra em uma Aba, digite "$Sair" para retornar para janela de Abas e após, digite '
                    f'"$Timer" para entrar na aba do Cronometro ⏲️')

    if p_message == '$start' and TemporaryData.Counter == 3:
        if not TemporaryData.TimerOn:
            horaAtual = datetime.datetime.now()
            TemporaryData.StudyStart = horaAtual
            TemporaryData.horaTemporaria = horaAtual
            TemporaryData.TimerOn = True
            return f'Cronometro iniciado as {horaAtual.hour} horas e {horaAtual.minute} minutos'
        else:
            return f'Já existe um cronomêtro ativo, finalize o crônometro atual usando "$Stop" para iniciar outro'

    if p_message == '$stop' and TemporaryData.Counter == 3:
        if TemporaryData.TimerOn:
            horaAtual = datetime.datetime.now()
            TemporaryData.StudyEnd = horaAtual
            tempoEstudado = horaAtual - TemporaryData.horaTemporaria
            tempoEstudado = tempoEstudado.total_seconds()
            tempoEstudado += TemporaryData.segundosTotais

            if tempoEstudado >= 3600:
                while tempoEstudado >= 3600:
                    tempoEstudado -= 3600
                    TemporaryData.horasTotais += 1

            if tempoEstudado >= 60:
                while tempoEstudado >= 60:
                    tempoEstudado -= 60
                    TemporaryData.minutosTotais += 1
            comando = (f'INSERT INTO studytime (Inicio, Fim, HorasEstudadas, MinutosEstudados) VALUES '
                       f'("{TemporaryData.StudyStart}", "{TemporaryData.StudyEnd}", {TemporaryData.horasTotais}, '
                       f'{TemporaryData.minutosTotais})')
            cursor.execute(comando)
            conexao.commit()
            TemporaryData.TimerOn = False
            return (f'Você estudou {TemporaryData.horasTotais} horas e {TemporaryData.minutosTotais} minutos na Data '
                    f'{TemporaryData.StudyStart.day}/{TemporaryData.StudyStart.month}/{TemporaryData.StudyStart.year}')
        else:
            return f'Não existe nenhum cronomêtro ativo no momento, digite "$Start" para iniciar um cronomêtro'

    if p_message == '$pause' and TemporaryData.Counter == 3:
        if TemporaryData.TimerOn:
            horaAtual = datetime.datetime.now()
            tempoEstudado = horaAtual - TemporaryData.horaTemporaria
            tempoEstudado = tempoEstudado.total_seconds()
            TemporaryData.segundosTotais = tempoEstudado
            TemporaryData.TimerOn = False
            return (f'Estudo pausado as {horaAtual.hour} horas e {horaAtual.minute} minutos\n\nDigite "$Start" para'
                    f' retornar de onde parou ou $stop para finalizar o crônometro')
        else:
            return f'Não existe nenhum cronomêtro ativo no momento, digite "$Start" para iniciar um cronomêtro'

    if TemporaryData.Counter == 3 and p_message == '$showall':
        comando = f'SELECT * FROM studytime'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        retorno = f'Histórico de Estudo: \n\n'
        for x in resultado:
            retornoacomp = f'ID:{x[0]} - Inicio: {x[1]} - Fim: {x[2]} - Tempo Estudado: {x[3]} Horas e {x[4]} Minutos\n'
            retorno += retornoacomp
        return f'{retorno}'

    if TemporaryData.Counter == 3 and p_message[:6] == '$show:':
        messageSplit = message[6:].split("/")
        print(messageSplit)
        DataLook = f"{messageSplit[2]}-{messageSplit[1]}-{messageSplit[0]}"
        comando = f'SELECT Inicio FROM studytime'
        cursor.execute(comando)
        datas = []
        retorno = f'Histórico de Estudos da Data {message[6:]}\n\n'
        resultado = cursor.fetchall()
        for x in resultado:
            if x[0][:10] == DataLook:
                datas.append(x)
        for x in datas:
            search = x[0]
            comando = f'SELECT * FROM studytime WHERE Inicio = "{search}"'
            cursor.execute(comando)
            resultado = cursor.fetchall()
            retorno += (f'ID: {resultado[0][0]} - Inicio: {resultado[0][1]} - Fim:{resultado[0][2]} - '
                        f'Tempo Estudado: {resultado[0][3]} Horas e {resultado[0][4]} Minutos\n')
        return f'{retorno}'

    if p_message[0:9] == '$list-in:' and TemporaryData.Counter == 2:

        comando = f'INSERT INTO listaconteudo (ConteudoArm) VALUES ("{message[9:]}")'
        cursor.execute(comando)
        conexao.commit()
        comando2 = f'SELECT idListaConteudo FROM listaconteudo WHERE ConteudoArm = ("{message[9:]}")'
        cursor.execute(comando2)
        chave = cursor.fetchall()
        return (f"Conteudo de Estudo armazenado com Sucesso!\nChave de acesso: {chave[0][0]}"
                f"\nContéudo Salvo: {message[9:]}")

    if p_message == '$list-on' and TemporaryData.Counter == 2:
        comando = f'SELECT * FROM listaconteudo'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        conteudoLista = f'Conteudos Armazenados: \n\n'
        for x in resultado:
            complementolistacomp = f'{x[0]} - {x[1]}\n'
            conteudoLista += complementolistacomp
        return f'{conteudoLista}'

    if p_message[:10] == '$list-out:' and TemporaryData.Counter == 2:
        comando = f'DELETE FROM listaconteudo WHERE idListaConteudo = {int(message[10:])}'
        cursor.execute(comando)
        conexao.commit()
        return f'Foi retirado com Sucesso o contéudo de Chave de acesso: {p_message[10:]}'

    if p_message == '$todolist':
        if TemporaryData.Counter == 0:
            TemporaryData.Counter = 1
            return (f'Você entrou na aba de criação de Listas de Tarefas 📝\n\nEscolha uma das seguintes opções:\n\n'
                    f'-> Digite: "$Create:(NomeDaLista),(MatériaDaLista)" para criar uma ToDoList\n'
                    f'-> Digite: "$Show:(IDdaLista)" para Verificar todos os Itens da ToDoList\n'
                    f'-> Digite: "$ShowAll" para Verificar todas as ToDoList´s\n'
                    f'-> Digite: "$AddTo:(IDdaLista),(Tarefa)" para adicionar uma tarefa a ToDoList\n'
                    f'-> Digite: "$RemoveFrom:(IDdaLista),(IDdaAtividade)" para remover uma atividade da ToDoList\n'
                    f'-> Digite: "$RemoveList:(IDdaLista)" para remover uma ToDoList\n'
                    f'-> Digite: "$Sair" para voltar para a Aba de funcionalidades')
        else:
            return (f'Você já se encontra em uma Aba, digite "$Sair" para retornar para janela de Abas e após, digite '
                    f'$"ToDoList" para entrar na aba de criação de Listas de Tarefas 📝')

    if TemporaryData.Counter == 1 and p_message[:8] == '$create:':
        messageSplit = message[8:].split(",")
        TemporaryData.IdCounter += 1
        comando = (f'INSERT INTO listtodolists (NomeTodoList, MateriaTodoList) VALUES ("{messageSplit[0]}",'
                   f' "{messageSplit[1]}")')
        cursor.execute(comando)
        conexao.commit()
        comando2 = f'INSERT INTO todolist (ToDoList) VALUES ("")'
        cursor.execute(comando2)
        conexao.commit()
        return (f'Criada Lista de Tarefas!!\nID - {TemporaryData.IdCounter}\nNOME - {messageSplit[0]}'
                f'\nMATÉRIA - {messageSplit[1]}')

    if TemporaryData.Counter == 1 and p_message[:6] == '$show:':
        messageInt = int(p_message[6:])
        comando = f'SELECT ToDoList FROM todolist WHERE IdToDoList = {messageInt}'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        conteudoLista = f'Tarefas a Fazer: \n\n'
        z = 0
        Tarefas = resultado[0][0]
        TarefasSeparadas = Tarefas.split("-")
        for x in TarefasSeparadas:
            if x != "":
                z += 1
                complementolistacomp = f'{z} - {x}\n'
                conteudoLista += complementolistacomp
                print(conteudoLista)
        return f'{conteudoLista}'

    if TemporaryData.Counter == 1 and p_message == '$showall':
        comando = f'SELECT * FROM listtodolists'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        retorno = f'Listas de Tarefas: \n\n'
        for x in resultado:
            retornoacomp = f'ID:{x[0]} - NOME: {x[1]} - MATÉRIA: {x[2]} \n'
            retorno += retornoacomp
        return f'{retorno}'

    if TemporaryData.Counter == 1 and p_message[:7] == '$addto:':
        messageSplit = message[7:].split(",")
        messageInt = int(messageSplit[0])
        comando = f'SELECT ToDoList FROM todolist WHERE IdToDoList = {messageInt}'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        Tarefas = resultado[0][0]
        formatado = messageSplit[1] + "-"
        Tarefas += formatado
        comando2 = f'UPDATE todolist SET ToDoList = ("{Tarefas}") WHERE IdToDoList = {messageInt}'
        cursor.execute(comando2)
        conexao.commit()
        return (f'Tarefa de Conteudo: {messageSplit[1]}\n'
                f'Adicionada com Sucesso!')

    if TemporaryData.Counter == 1 and p_message[:12] == '$removefrom:':
        messageSplit = message[12:].split(",")
        messageInt = int(messageSplit[0])
        messageInt2 = int(messageSplit[1])
        comando = f'SELECT ToDoList FROM todolist WHERE IdToDoList = {messageInt}'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        Tarefas = resultado[0][0]
        TarefasSeparadas = Tarefas.split("-")
        NumRemover = messageInt2 - 1
        TarefasSeparadas.pop(NumRemover)
        print(TarefasSeparadas)
        Total = ""
        for x in TarefasSeparadas:
            if x != "":
                Total += f'{x}-'
        comando2 = f'UPDATE todolist SET ToDoList = ("{Total}") WHERE IdToDoList = {messageInt}'
        cursor.execute(comando2)
        conexao.commit()
        return f'Foi removida a Tarefa de ID: {messageSplit[1]}'

    if TemporaryData.Counter == 1 and p_message[:12] == '$removelist:':
        messageSplit = int(message[12:])
        comando = f'SELECT * FROM listtodolists WHERE IdsLists = {messageSplit}'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        comando = f'DELETE FROM todolist WHERE IdToDoList = {messageSplit}'
        cursor.execute(comando)
        conexao.commit()
        comando = f'DELETE FROM listtodolists WHERE IdsLists = {messageSplit}'
        cursor.execute(comando)
        conexao.commit()
        return (f'Foi Removido a ToDoList de ID:{resultado[0][0]} - NOME:{resultado[0][1]} - '
                f'MATÉRIA:{resultado[0][2]}')

    if TemporaryData.Counter != 0 and p_message == "$sair":
        TemporaryData.Counter = 0
        return ('Essas são as minhas funções principais:'
                '\n1 - Digite: "$Timer" para acessar a aba do Crômetro'
                '\n2 - Digite: "$ContentList" para acessar a aba de Conteúdo de Estudo'
                '\n3 - Digite: "$ToDoList" para acessar a aba de ListaDeTarefas'
                '\n4 - Digite: "$DuvidasIA" para tirar Duvidas com a inteligência Artificial da Google')

    if p_message[0] == '$' and TemporaryData.Counter == 4:
        cmessage = message[1:]
        resposta = (bard.get_answer(cmessage)['content'])
        return f'{resposta}'

    if p_message[0] == '$':
        return 'Nenhum comando válido inserido'
