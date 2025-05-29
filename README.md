
# Start ElasticSearch service
```bash
cd rag-services
docker-compose up -d
```

# How to download documents
```bash
mkdir documents
curl --output "documents/agile-po-prostu-ebook.pdf" --url "https://projectmakers.pl/wp-content/uploads/2024/01/agile-po-prostu-ebook.pdf"
curl --output "documents/2020-Scrum-Guide-Polish.pdf" --url "https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-Polish.pdf"
```

# Create env
```bash
python -m venv venv
source venv/bin/activate
pip install -r resources.txt
# rename env to .env
# set OPENAI_API_KEY
```

# Load data into system
```bash
(venv) >python -m app.loader
```

# Ask system
```text
(venv) >python -m app.query
Enter a query (or 'done' to finish): Czym różni się Agile od Scrum'a? 
Agile to ogólna filozofia i podejście do zarządzania projektami, które opiera się na iteracyjnym i przyrostowym działaniu, skupiając się na szybkim dostarczaniu wartości i zbieraniu informacji zwrotnej. Scrum natomiast jest konkretnym ramem postępowania w ramach Agile, opartym na empiryzmie i koncepcji lean, kt
óre definiują strukturę, role, wydarzenia i praktyki umożliwiające realizację projektów zgodnie z zasadami Agile.

Enter a query (or 'done' to finish): Co to jest Agile?                
Agile to podejście do zarządzania projektami, które polega na częstym wydawaniu działających wersji produktu, zbieraniu i uwzględnianiu informacji zwrotnej w iteracjach. Działa najlepiej, gdy wiadomo, co chce się osiągnąć, i gdy istnieje potrzeba elastycznego dostosowania się do zmian. W praktyce Agile obejmuje
 dostosowywanie procesów do potrzeb, eliminowanie zbędnych działań oraz łączenie elementów tradycyjnych i zwinnych metod w celu osiągnięcia efektywnych rezultatów.
 
Enter a query (or 'done' to finish): Co to jest Sprint?
Sprint to ustalony, krótkotrwały okres, zwykle trwający maksymalnie miesiąc, podczas którego zespół Scrum realizuje określony zakres pracy, aby osiągnąć cel Sprintu. W trakcie Sprintu nie wprowadza się zmian mogących zagrozić realizacji tego celu, a praca jest planowana, inspekcjonowana i dostosowywana na bieżą
co. Sprint obejmuje wydarzenia takie jak Sprint Planning, Daily Scrum, Sprint Review oraz Sprint Retrospective, które wspierają efektywną realizację celów i ciągłe doskonalenie procesu.

Enter a query (or 'done' to finish): Jak duży powinien być zespół w Scrum?
Zespół Scrum powinien być wystarczająco mały, aby pozostać zwinnym i efektywnym, zwykle składa się z około 10 osób lub mniej. Mniejsze zespoły lepiej się komunikują i są bardziej produktywne, natomiast jeśli zespół staje się zbyt duży, warto rozważyć podział na kilka spójnych Scrum Teamów skupionych na tym samy
m produkcie i mających wspólny cel, Product Backlog oraz Product Ownera.

Enter a query (or 'done' to finish): Jak duży powinien być zespół w Agile? 
W metodologii Agile nie ma jednoznacznej, sztywnej wielkości zespołu, ale zazwyczaj zaleca się, aby był on na tyle mały, aby zapewnić efektywną komunikację i współpracę. Optymalna liczba to zwykle od 3 do 9 osób, co pozwala na skuteczne samoorganizowanie się i szybkie podejmowanie decyzji.

Enter a query (or 'done' to finish): Jakie jest zadanie Scrum Master'a?    
Scrum Master jest odpowiedzialny za zapewnienie, aby Scrum był stosowany zgodnie z opisem w przewodniku. Pomaga wszystkim w zrozumieniu teorii i praktyki Scrum, wspiera efektywność zespołu, tworzy odpowiednie warunki do poprawy praktyk, usuwa przyczyny ograniczające postępy zespołu, dba o przebieg wydarzeń Scru
m, instruuje członków zespołu na temat samozarządzania i interdyscyplinarności, pomaga skupić się na tworzeniu wartościowych Incrementów, wspiera Product Ownera w zarządzaniu Product Backlogiem, a także wspiera organizację w wdrażaniu Scrum i usuwa bariery między interesariuszami a zespołem.

Enter a query (or 'done' to finish): done
```

# Documentation
```text
Chunking
https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_double_merging_chunking/
https://bitpeak.pl/chunking-methods-in-rag-methods-comparison/
https://medium.com/@sayantanmanna840/rag-chunking-strategies-with-llamaindex-optimizing-your-retrieval-pipeline-6fdb9f0d50c2

https://docs.llamaindex.ai/en/stable/examples/vector_stores/Elasticsearch_demo/
https://docs.llamaindex.ai/en/stable/examples/vector_stores/ElasticsearchIndexDemo/

```
