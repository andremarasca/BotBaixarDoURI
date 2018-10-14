from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.urionlinejudge.com.br')

email = driver.find_element_by_id('email')
email.send_keys("insira aqui seu e-mail")

password = driver.find_element_by_id('password')
password.send_keys("insira aqui sua senha")

submit = driver.find_element_by_class_name('submit')
submit.click()

#%% Descobrir quais eu fiz

import os

categoria = 1
while True:
    ex_resolvidos = []
    pagina = 1
    driver.get('https://www.urionlinejudge.com.br/judge/pt/problems/index/%d?page=%d' %(categoria, pagina))
    try:
        driver.find_element_by_class_name('website-mode')
    except:
        break
    while True:
        driver.get('https://www.urionlinejudge.com.br/judge/pt/problems/index/%d?page=%d' %(categoria, pagina))
        try:
            driver.find_element_by_class_name('website-mode')
            print('Pagina %d' %pagina)
        except:
            break

        n = 1
        while True:
            try:
                nome_ex = driver.find_element_by_xpath('//*[@id="element"]/table/tbody/tr[%d]/td[1]/a' %n)
            except:
                break

            n_ex = int(nome_ex.text)
            try:
                linha = driver.find_element_by_xpath('//*[@id="element"]/table/tbody/tr[%d]/td[2]/img' %n)
                if linha.get_attribute('src') == 'https://urionlinejudge.r.worldssl.net/judge/img/5.0/solved.png?1452205133':
                    print('%d fez' %n_ex)
                    ex_resolvidos.append(n_ex)
                else:
                    print('%d fez errado' %n_ex)
            except:
                print('%d nao fez' %n_ex)
            n += 1
        pagina += 1


    directory = 'Categoria %d' %categoria

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    # baixa os exercicios
    for exercicio in ex_resolvidos:
        link = 'https://www.urionlinejudge.com.br/judge/pt/problems/view/%d' %exercicio
        driver.get(link)

        submissao = driver.find_element_by_xpath('//*[@id="place"]/a')
        link_codigo = submissao.get_attribute('href')
        driver.get(link_codigo)

        codigo = driver.find_element_by_class_name('ace_content')
        meu_codigo = codigo.text

        while len(meu_codigo) == 0:
            codigo = driver.find_element_by_class_name('ace_content')
            meu_codigo = codigo.text

        if len(meu_codigo.split('\n')) <= 25:

            if meu_codigo.find('main') > 0:
                text_file = open(directory + "\\%d.c" %exercicio, "w")
            else:
                text_file = open(directory + "\\%d.py" %exercicio, "w")

            text_file.write(meu_codigo)

            text_file.close()

    categoria += 1