import datetime
import TemporaryData
import bot


def handle_responses(message) -> str:
    p_message = message.lower()

    if p_message == '$hello':
        return ('Olá, eu sou o Tudy 🤓, o BOT de Estudos!!\n'
                'Essas são as minhas funções principais:'
                '\n1 - Digite: "$Timer" para acessar a aba do Crômetro'
                '\n2 - Digite: "$ContentList" para acessar a aba de Conteúdo de Estudo'
                '\n3 - Digite: "$ToDoList" para acessar a aba de ListaDeTarefas')

    if p_message == "$contentlist" and TemporaryData.Counter == 0:
        TemporaryData.Counter = 2
        return (f'Você entrou na aba de Listas de Conteudos 🧠\n\nEscolha uma das seguintes opções:\n\n'
                f'-> Digite:"$List-in:(Conteudo)" para inserir conteudo na Lista de Conteudos\n'
                f'-> Digite:"$List-on" para ver os conteudos na Lista de Conteudos\n'
                f'-> Digite:"$List-out:(IDdoConteudo)" para retirar conteudo da Lista de Conteudos\n'
                f'-> Digite:"$Sair" para voltar para a Aba de funcionalidades\n')

    if p_message == "$timer" and TemporaryData.Counter == 0:
        TemporaryData.Counter = 3
        return (f'Você entrou na aba do Cronometro ⏲️\n\nEscolha uma das seguintes opções:\n\n'
                f'-> Digite:"$Start" para iniciar o Cronômetro\n'
                f'-> Digite:"$Stop" para finalizar o Cronômetro\n'
                f'-> Digite:"$Pause" para pausar o Cronômetro\n'
                f'-> Digite:"$Sair" para voltar para a Aba de funcionalidades\n')

    if p_message == '$start' and TemporaryData.Counter == 3:
        horaAtual = datetime.datetime.now()
        TemporaryData.horaTemporaria = horaAtual
        return f'Cronometro iniciado as {horaAtual.hour} horas e {horaAtual.minute} minutos'

    if p_message == '$stop' and TemporaryData.Counter == 3:
        horaAtual = datetime.datetime.now()
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

        return f'Você estudou {TemporaryData.horasTotais} horas e {TemporaryData.minutosTotais} minutos'

    if p_message == '$pause' and TemporaryData.Counter == 3:
        horaAtual = datetime.datetime.now()
        tempoEstudado = horaAtual - TemporaryData.horaTemporaria
        tempoEstudado = tempoEstudado.total_seconds()
        TemporaryData.segundosTotais = tempoEstudado
        return (f'Estudo pausado as {horaAtual.hour} horas e {horaAtual.minute} minutos\n\nDigite $start para'
                f'\n retornar de onde parou ou $stop para finalizar o crônometro')

    if p_message[0:9] == '$list-in:' and TemporaryData.Counter == 2:
        Chave = (len(TemporaryData.Conteudos)) + 1
        TemporaryData.Conteudos.update({Chave: message[9:]})
        return (f"Conteudo de Estudo armazenado com Sucesso!\nChave de acesso: {Chave}"
                f"\nContéudo Salvo: {message[9:]}")

    if p_message == '$list-on' and TemporaryData.Counter == 2:
        listaConteudo = 'Conteudo Armazenado:\n'
        for chave, conteudo in TemporaryData.Conteudos.items():
            conteudoLista = f'{chave} - {conteudo}\n'
            listaConteudo = listaConteudo + conteudoLista

        return f'{listaConteudo}'

    if p_message[:10] == '$list-out:' and TemporaryData.Counter == 2:
        print(TemporaryData.Conteudos)
        TemporaryData.Conteudos.pop(int(p_message[10:]))
        print(TemporaryData.Conteudos)
        return f'Foi retirado com Sucesso o contéudo de Chave de acesso: {p_message[10:]}'

    if p_message == '$todolist' and TemporaryData.Counter == 0:
        TemporaryData.Counter = 1
        return (f'Você entrou na aba de criação de Listas de Tarefas 📝\n\nEscolha uma das seguintes opções:\n\n'
                f'-> Digite: "$Create:(NomeDaLista),(MatériaDaLista)" para criar uma ToDoList\n'
                f'-> Digite: "$Show:(IDdaLista)" para Verificar todos os Itens da ToDoList\n'
                f'-> Digite: "$ShowAll" para Verificar todas as ToDoList´s\n'
                f'-> Digite: "$AddTo:(IDdaLista),(Tarefa)" para adicionar uma tarefa a ToDoList\n'
                f'-> Digite: "$RemoveFrom:(IDdaLista),(IDdaAtividade)" para remover uma atividade da ToDoList\n'
                f'-> Digite: "$RemoveList:(IDdaLista)" para remover uma ToDoList\n'
                f'-> Digite: "$Sair" para voltar para a Aba de funcionalidades')

    if TemporaryData.Counter == 1 and p_message[:8] == '$create:':
        messageSplit = message[8:].split(",")
        ToDoDict = {0: messageSplit}
        TemporaryData.ToDoDictAll.update({TemporaryData.IdDict: ToDoDict})
        TemporaryData.IdDict += 1
        return (f'Lista de Tarefas criada com Sucesso!\nID: {TemporaryData.IdDict - 1}\nNome: {messageSplit[0]}\n'
                f'Matéria: {messageSplit[1]}')

    if TemporaryData.Counter == 1 and p_message[:6] == '$show:':
        messageInt = int(p_message[6:])
        Retorno = (f'Nome da ToDoList: {TemporaryData.ToDoDictAll[messageInt][0][0]} - Matéria: '
                   f'{TemporaryData.ToDoDictAll[messageInt][0][1]}\n')
        for x in range(1, len(TemporaryData.ToDoDictAll[messageInt])):
            Retorno += f'{x} - {TemporaryData.ToDoDictAll[messageInt][x]}\n'
        return Retorno

    if TemporaryData.Counter == 1 and p_message == '$showall':
        Retorno = 'Todas as ToDoList:\n'
        for x in range(0, len(TemporaryData.ToDoDictAll)):
            Retorno += (f'-> Id: {x} - Nome: {TemporaryData.ToDoDictAll[x][0][0]} -'
                        f' Matéria: {TemporaryData.ToDoDictAll[x][0][1]}\n')
        return f'{Retorno}'

    if TemporaryData.Counter == 1 and p_message[:7] == '$addto:':
        messageSplit = message[7:].split(",")
        messageInt = int(messageSplit[0])
        IdUsado = len(TemporaryData.ToDoDictAll[messageInt])
        NovoDado = {IdUsado: messageSplit[1]}
        TemporaryData.ToDoDictAll[messageInt].update(NovoDado)
        return (f'Tarefa Adicionada com Sucesso!\n'
                f'{IdUsado} - {messageSplit[1]}')

    if TemporaryData.Counter == 1 and p_message[:12] == '$removefrom:':
        messageSplit = message[12:].split(",")
        Tarefa = TemporaryData.ToDoDictAll[int(messageSplit[0])][int(messageSplit[1])]
        TemporaryData.ToDoDictAll[int(messageSplit[0])].pop(int(messageSplit[1]))
        return f'Foi removida a Tarefa de ID: {messageSplit[1]} - TAREFA: {Tarefa}'

    if TemporaryData.Counter == 1 and p_message[:12] == '$removelist:':
        messageSplit = int(message[12:])
        Excluido = TemporaryData.ToDoDictAll[messageSplit]
        TemporaryData.ToDoDictAll.pop(messageSplit)
        return f'Foi Removido a ToDoList de ID:{messageSplit} - NOME:{Excluido[0][0]} - MATÉRIA:{Excluido[0][1]}'

    if TemporaryData.Counter != 0 and p_message == "$sair":
        TemporaryData.Counter = 0
        return ('Essas são as minhas funções principais:'
                '\n1 - Digite: "$Timer" para acessar a aba do Crômetro'
                '\n2 - Digite: "$ContentList" para acessar a aba de Conteúdo de Estudo'
                '\n3 - Digite: "$ToDoList" para acessar a aba de ListaDeTarefas')
