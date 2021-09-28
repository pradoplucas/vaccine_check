import requests, csv, json, os, datetime, argparse, sys
from tabulate import tabulate

city_ = 'nova fatima'
#city_ = 'bandeirantes'
#city_ = 'cornelio procopio'
#city_ = 'londrina'

parser = argparse.ArgumentParser(description = 'Como está a vacinação na sua cidade?')

parser.add_argument('-c', action = 'store', dest = 'city', help = 'city name, lowercase and without accent', default = city_)

args = parser.parse_args()

city = args.city

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def select_city():
    res = requests.get("http://201.77.18.66/Exportacao/vacinacaoranking.csv").text
    open('./last/res.csv', 'wt').write(res)

    with open('./last/res.csv', newline='') as csvfile:
        resCSV = csv.DictReader(csvfile, delimiter=';')

        for row in resCSV:
            if(row['Município_Vacina'] == city.upper()):
                return row

    print('Cidade não encontrada.')

    sys.exit()

def format_data(dict_data):

    dict_data["Doses Recebidas pelos Munc\u00edpios"] = int(dict_data["Doses Recebidas pelos Munc\u00edpios"])
    
    dict_data["Disribuido 1\u00aa Dose "] = int(dict_data["Disribuido 1\u00aa Dose "])
    
    dict_data["Aplica\u00e7\u00f5es 1\u00aa Dose "] = int(dict_data["Aplica\u00e7\u00f5es 1\u00aa Dose "])
    
    dict_data["% Distrib. 1\u00aa Dose"] = float(dict_data["% Distrib. 1\u00aa Dose"].rstrip("%").replace(",", "."))
    
    dict_data["Disribuido 2\u00aa Dose "] = int(dict_data["Disribuido 2\u00aa Dose "])
    
    dict_data["Aplica\u00e7\u00f5es 2\u00aa Dose "] = int(dict_data["Aplica\u00e7\u00f5es 2\u00aa Dose "])
    
    dict_data["% Distrib 2\u00aa Dose"] = float(dict_data["% Distrib 2\u00aa Dose"].rstrip("%").replace(",", "."))

    dict_data["Popula\u00e7\u00e3o Censo 2010"] = int(dict_data["Popula\u00e7\u00e3o Censo 2010"])

    dict_data["Popula\u00e7\u00e3o Estimada 2020"] = int(dict_data["Popula\u00e7\u00e3o Estimada 2020"])

    dict_data['% Vacinados 1\u00aa Dose'] = dict_data["Aplica\u00e7\u00f5es 1\u00aa Dose "]*100/dict_data["Popula\u00e7\u00e3o Estimada 2020"]

    dict_data['% Vacinados 2\u00aa Dose'] = dict_data["Aplica\u00e7\u00f5es 2\u00aa Dose "]*100/dict_data["Popula\u00e7\u00e3o Estimada 2020"]

    return dict_data

def create_table(now, old):
    #Att
    list_now = [now['Atualizado em ']]
    list_before = [old['Atualizado em ']]
    
    info1 = {'Agora': list_now, 'Antes': list_before}
    table1 = tabulate(info1, headers='keys', tablefmt="grid", colalign=("center","center") )
    info2 = {'Atualização' : [table1]}

    att = tabulate(info2, headers='keys', tablefmt="pretty")

    #Doses Recebidas
    list_now = [now["Doses Recebidas pelos Muncípios"]]
    list_before = [old["Doses Recebidas pelos Muncípios"]]
    list_diff = [now["Doses Recebidas pelos Muncípios"] - old["Doses Recebidas pelos Muncípios"]]
    
    info1 = {'': ['Recebidas'], 'Agora': list_now, 'Antes': list_before, 'Diff': list_diff}
    table1 = tabulate(info1, headers='keys', tablefmt="grid", colalign=("center","center","center","center") )
    info2 = {'Doses' : [table1]}

    doses_recebidas = tabulate(info2, headers='keys', tablefmt="pretty")

    #1a Dose
    list_now = [now["Disribuido 1ª Dose "], now["Aplicações 1ª Dose "], str(round(now["% Distrib. 1ª Dose"], 2)) + '%']
    list_before = [old["Disribuido 1ª Dose "], old["Aplicações 1ª Dose "], str(round(old["% Distrib. 1ª Dose"], 2)) + '%']
    list_diff = [now["Disribuido 1ª Dose "] - old["Disribuido 1ª Dose "], now["Aplicações 1ª Dose "] - old["Aplicações 1ª Dose "], str(round(now["% Distrib. 1ª Dose"] - old["% Distrib. 1ª Dose"], 2)) + '%' ]
    
    info1 = {'': ['Distribuidas', 'Aplicadas', '(%)'], 'Agora': list_now, 'Antes': list_before, 'Diff': list_diff}
    table1 = tabulate(info1, headers='keys', tablefmt="grid", colalign=("center","center","center","center") )
    info2 = {'1ªas Doses': [table1]}

    doses_1 = tabulate(info2, headers='keys', tablefmt="pretty")

    #2a Dose
    list_now = [now["Disribuido 2ª Dose "], now["Aplicações 2ª Dose "], str(round(now["% Distrib 2ª Dose"], 2)) + '%']
    list_before = [old["Disribuido 2ª Dose "], old["Aplicações 2ª Dose "], str(round(old["% Distrib 2ª Dose"], 2)) + '%']
    list_diff = [now["Disribuido 2ª Dose "] - old["Disribuido 2ª Dose "], now["Aplicações 2ª Dose "] - old["Aplicações 2ª Dose "], str(round(now["% Distrib 2ª Dose"] - old["% Distrib 2ª Dose"], 2)) + '%' ]
    
    info1 = {'': ['Distribuidas', 'Aplicadas', '(%)'], 'Agora': list_now, 'Antes': list_before, 'Diff': list_diff}
    table1 = tabulate(info1, headers='keys', tablefmt="grid", colalign=("center","center","center","center") )
    info2 = {'2ªas Doses': [table1]}

    doses_2 = tabulate(info2, headers='keys', tablefmt="pretty")

    #Vacinados
    list_now = [str(round(now['% Vacinados 1\u00aa Dose'], 2)) + '%', str(round(now['% Vacinados 2\u00aa Dose'], 2)) + '%']
    list_before = [str(round(old['% Vacinados 1\u00aa Dose'], 2)) + '%', str(round(old['% Vacinados 2\u00aa Dose'], 2)) + '%']
    list_diff = [str(round(now['% Vacinados 1\u00aa Dose'] - old['% Vacinados 1\u00aa Dose'], 2)) + '%', str(round(now['% Vacinados 2\u00aa Dose'] - old['% Vacinados 2\u00aa Dose'], 2)) + '%']
    
    info1 = {'': ['1ª Dose', '2ª Dose'], 'Agora': list_now, 'Antes': list_before, 'Diff': list_diff}
    table1 = tabulate(info1, headers='keys', tablefmt="grid", colalign=("center","center","center","center") )
    info2 = {'Vacinados': [table1]}

    vacinados = tabulate(info2, headers='keys', tablefmt="pretty")

    #All
    res_all = att + '\n\n' + doses_recebidas + '\n\n' + doses_1 + '\n\n' + doses_2 + '\n\n' + vacinados

    info = {now["Município_Vacina"].strip() + ' - ' + str(now["População Estimada 2020"]) + ' habitantes' : [res_all]}

    return tabulate(info, headers='keys', tablefmt="pretty")

def main():
    dict_now = format_data(select_city())

    if(not os.path.isfile('./actual/' + city +'.json')):
        open('./actual/' + city + '.json', 'wt').write(json.dumps(dict_now))
        open('./last/' + city + '.json', 'wt').write(json.dumps(dict_now))

    dict_old = json.loads(open('./actual/' + city + '.json').read())

    time_now = datetime.datetime.now()
    time_str = time_now.strftime("%H") + 'h' + time_now.strftime("%M") + 'm-' + time_now.strftime("%d") + time_now.strftime("%m") + time_now.strftime("%y")

    if(dict_old['Atualizado em '] != dict_now['Atualizado em ']):
        open('./old/' + city + '-' + time_str + '.json', 'wt').write(open('./last/' + city + '.json').read())
        open('./last/' + city + '.json', 'wt').write(json.dumps(dict_old))
        open('./actual/' + city + '.json', 'wt').write(json.dumps(dict_now))
    
    dict_old = json.loads(open('./last/' + city + '.json').read())

    res_table = create_table(dict_now, dict_old)

    open('./res/' + city + ' - ' + time_str + '.txt', 'wt').write(res_table)

    print(res_table)

    input()

if __name__ == '__main__':
    create_directory('old')
    create_directory('last')
    create_directory('actual')
    create_directory('res')
    main()
