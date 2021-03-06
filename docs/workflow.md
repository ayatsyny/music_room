# Workflow


## Опис

Є дві основні гілки:

* **master** -- гілка з версіями стабільних релізів, що деплоється на продакшн.
* **develop** -- гілка з тестовими робочими версіями, що деплоєтья на тестовий
сервер. Час від часу відбуваєтсья злиття (*merge*) *develop* -&gt; *master* для
випуску нових релізів. 


В *develop* потрапляють лише завершені та робочі зміни.


## Внесення основних змін в код

Сюди включається основна розробка над поектом.

* Оновити локальну гілку *develop* до останньої версії.
* Створити нову розробницьку гілку на основі *develop*, наприклад *newfeature*.
Бажано, щоб назва нової гілки була інформативна та асоціювалась зі змінами,
які вона вносить.
* Вносити зміни в розробницьку гілку, періодично робити *commit* та *push* на
центральний репозиторій. Бажано, щоб назва гілки на локальному та центральному
репозиторії співпадала.
* В будь-який момент (бажано після перших *commit*), зробити *merge-request*
розробницької гілки на гілку *develop*. Це дозволить іншим учасникам переглядати
внесені зміни та обговорювати їх (code review), а також запускати автоматизовані
тести. Якщо робота з гілкою довготривала, тоді бажано час від часу зливатись
з гілкою *develop*, щоб не сильно віддалятись від основної гілки проекту.
* Після завершеня роботи над розробницькою гілкою, злити її з останньою версією
гілки *develop* (виправивши всі конфлікти, які можуть виникнути), зробити
*commit* та *push* і повідомити ведучого програміста про готовність *merge*.
Це можна зробити напряму або залишивши повідомленя в коментарях *merge-request*.

Після *merge* розробницької гілки з гілкою *develop*, розробницька гілка має бути
видалена на центральному репозиторії. Після оновлення локального репозиторія
неіснуючі гілки теж бажано видалити.


## Внесення термінових змін (hotfix)

Сюди включаються невеликі поправки, які необхідно швидко включити в продакшн.
Як правило, це виправлення помилок.

* Оновити локальну гілку *master* до останньої версії.
* Створити нову розробницьку гілку на основі *master* з префіксом *hotfix-*
в назві, наприклад, *hotfix-somefeature*.
* Вносити зміни в розробницьку гілку, періодично робити *commit* та *push* на
центральний репозиторій. Бажано, щоб назва гілки на локальному та центральному
репозиторії співпадала.
* В будь-який момент (бажано після перших *commit*), зробити *merge-request*
розробницької гілки на гілку *master* та *develop*. Це дозволить іншим учасникам
переглядати внесені зміни та обговорювати їх (code review), а також запускати
автоматизовані тести.
* Після завершеня роботи над розробницькою гілкою зробити *commit* та *push* і
повідомити ведучого програміста про готовність *merge*.

Після *merge* розробницької гілки з гілкою *master* та *develop*, розробницька
гілка має бути видалена на центральному репозиторії. Після оновлення локального
репозиторія неіснуючі гілки теж бажано видалити.


## Команди GIT


### branch & checkout

Перегляд списку гілок:
    
    git branch     # список локальних гілок
    git branch -a  # список локальних та віддалених гілок
    
Створення нової гілки на основі локальної активної гілки:

    git branch new-branch  # створить локальну гілку new-branch на базі активної
    
Переключення між гілками:

    git checkout new-branch  # переключить на гілку new-branch
  
Якщо при переключенні активна гілка має незакомічені зміни, тоді буде відображатись помилка.
Щоб ігнорувати (видалити) зміни і переключитись -- треба додати ключ `-f`:

    git checkout -f new-branch  # переключить на new-branch ігноруючи незакомічені зміни активної гілки
    
Створення нової гілки на основі активної гілки та переключення на нову гілку:

    git checkout -b new-branch
    # виконає те ж саме, що дві наступні команди:
    git branch new-branch
    git checkout new-branch
    
Видалення локальної гілки:

    git branch -d new-branch  # видалить гілку new-branch, якщо вона не має незлитих змін (інакше буде помилка)
    git branch -D new-branch  # видалить гілку new-branch в будь-якому випадку

### fetch & merge

Оновляє віддалені гілки на локальному репозиторію без злиття їх з локальними гілками:

    git fetch         # оновлення з основного віддаленого репозиторія
    git fetch origin  # оновлення з віддаленого репозиторія origin

Після цієї команди зазвичай виконують злиття віддаленої гілки з локальною:

    git merge origin/master         # злиття віддал. гілки origin/master з локальною активною гілкою
    git merge master                # злиття локальної гілки master з локальною активною гілкою
    git merge origin/master master  # злиття віддал. гілки origin/master з локальною гілкою master

Якщо активна гілка *mybranch* і виконується команда `git merge master`,
то це означає, що локальна гілка *mybranch* буде оновлена змінами з локальної
гілки *master*. В результаті, якщо не буде конфліктів, в гілці *mybranch* буде
створений коміт, в якому будуть всі відмінності з гілки *master*.



todo:<br>
stash, add, commit, pull, push, clone
git push -u origin develop
