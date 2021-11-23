MetaPython: quando trocamos os encanamentos!

Python é versátil o suficiente para, sem quebrar as regras da linguagem, podermos implementar polimorfismo, tail recursion, lazy execution, checagem de tipos, atributos privados, mudar o "jeito" da linguagem para que lembre LISP, ou Forth, ou ainda fazer tudo em uma única expressão de uma linha. Usando os vários recursos entre metaclasses, decorators, introspecção dos frames de execução, são mostrados exemplos de cada uma dessas coisas for fun & profit.

* Function Decorators

Permitem processar um objeto função assim que ele é instanciado.

O processo permite mudar atributos de uma função,
 

permite fazer o ^wrap de uma função com código que
muodifica seu comportamento.


As vezes até entendemos o conceito,
mas não sabemos onde usar

Um exemplo simples, pode ser anotação de tipos.


def sum(a, b):
    if not is instance(a, int) or not isinstance(b, int):
        raise TypeError


<<static.py


* polimorfismo


Em linguagens estáticas se escreve várias
vezes um método
 
 para cada combinação possível de parâmetros.


Só com decorators de métodos - 
 
 
em vez de devolver uma função:
    
- manter um dicionário com o nome dos métodos estáticos já
registrados para cada classe


- devolver um objeto especial que: 
    -- com informação dos métodos homônimos e tipos de atributos
    -- um método __call__ que faça o dispatch adequado


Não pode ser feito exclusivamente com metaclasse
 

métodos com mesmo nome se sobrescreverem durante o parsing


só o último método definido seria passado aos wrappers de metaclasse


meta-classes para sinalizar uma nova classe, 


evitando que métodos de classes diferentes se confundam


<<polymorph.py


* Tail Recursion


No dia que fiz, achei um post do BDFL dizendo "não faça"


Escrito dois dias antes


Há várias implementações mais robustas também

Mas... #comofas? 

Com um @decorator -- anotamos que a função foi chamada

e realizamos a chamada original dentro de um try: except

Se, antes do retorno, houver outra chamada à mesma função
       anotamos os parâmetros
       levantamos uma exceção!
       
       e estamos de volta no contexto do decorator
       que pode realizar uma nova chamada
       
       com os parâmetros salvos, mas sem
       aumentar a profundidade da pilha


<<tailrecusion.py


* lazy execution


Um objeto python só "faz" alguma coisa quando 
é invocado um dos métodos "under under"


Basta um decorator que retorne um  objeto 
que se "lembre" da função e dos parâmetros usados


e disponibilize todos os métodos "under under"
do data_model

E só quando um dos métodos "under under" for chamado é que a
função original é executada.

<<lazy_decorator.py


* Atributos Privados


Em tese só podem ser acessados pela instância "dona" do atributo


implementamos nos hooks de acesso a atributos da
classe uma verificação de identidade


Para isso instropecta-se o frame apropriado
na pilha de execução


import sys
sys._getframe(level)


E verifica-se se quem chamou o método
para recuperar um atributo tem esse direito


<<privateattr.py


* Mudando a 'cara' da linguagem:

Não faça, exceto por diversão!


Para parcer Scheme, o principal é 
"define" coisas num grupo de parenteses externos


E funções de uma letra que usem os argumentos
como o scheme usa as listas


<<pyschemificator.py


* Programação Orientada a Aspectos

Uma forma de adicionar todo um tipo de comportamento 
a determinado grupo de métodos em sistemas já em funcionamento.


Com isso o código pode acumular muito código repetitivo


em logging, checagem de parâmetros, gerenciamento de cache,
verificação de integridade

A idéia de "aspect orientation" é permitir que comportamento comum 
fique num canto comum do código,
 
e, baseando-se apenas em tipos
de parâmetros, ou padrões no nome dos métodos, 
esse código comum seja executado apropriadamente.


Em Java, tiveram que criar um ^fork da linguagem, chamado "aspectj"
que inclui o tipo "aspect" ao lado de "classes" e "interfaces".


Em python, poderiamos usar só method decorators.


Existem várias implementações usando a introspecção de python
para cobrir aspect oriented programing para todos os gostos

Com metaclasses, podemos fazer em 100 linhas de código.

<<aspect.py

