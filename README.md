
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
# .\venv\activate
pip install -U -r resources.txt
python -m spacy download pl_core_news_md
# rename env to .env
# set OPENAI_API_KEY
```

# Load data into RAG system
```bash
(venv) >python -m app.loader
```

# Ask RAG system
```text
(venv) >python -m app.query
Enter a query (or 'done' to finish): Czym różni się Agile od Scrum'a? 
Agile to ogólna filozofia i podejście do zarządzania projektami, które opiera się na iteracyjnym i przyrostowym działaniu, skupiając się na szybkim dostarczaniu wartości i zbieraniu informacji zwrotnej. Scrum natomiast jest konkretnym ramem postępowania w ramach Agile, opartym na empiryzmie i koncepcji lean, które definiują strukturę, role, wydarzenia i praktyki umożliwiające realizację projektów zgodnie z zasadami Agile.

Enter a query (or 'done' to finish): Co to jest Agile?                
Agile to podejście do zarządzania projektami, które polega na częstym wydawaniu działających wersji produktu, zbieraniu i uwzględnianiu informacji zwrotnej w iteracjach. Działa najlepiej, gdy wiadomo, co chce się osiągnąć, i gdy istnieje potrzeba elastycznego dostosowania się do zmian. W praktyce Agile obejmuje dostosowywanie procesów do potrzeb, eliminowanie zbędnych działań oraz łączenie elementów tradycyjnych i zwinnych metod w celu osiągnięcia efektywnych rezultatów.
 
Enter a query (or 'done' to finish): Co to jest Sprint?
Sprint to ustalony, krótkotrwały okres, zwykle trwający maksymalnie miesiąc, podczas którego zespół Scrum realizuje określony zakres pracy, aby osiągnąć cel Sprintu. W trakcie Sprintu nie wprowadza się zmian mogących zagrozić realizacji tego celu, a praca jest planowana, inspekcjonowana i dostosowywana na bieżąco. Sprint obejmuje wydarzenia takie jak Sprint Planning, Daily Scrum, Sprint Review oraz Sprint Retrospective, które wspierają efektywną realizację celów i ciągłe doskonalenie procesu.

Enter a query (or 'done' to finish): Jak duży powinien być zespół w Scrum?
Zespół Scrum powinien być wystarczająco mały, aby pozostać zwinnym i efektywnym, zwykle składa się z około 10 osób lub mniej. Mniejsze zespoły lepiej się komunikują i są bardziej produktywne, natomiast jeśli zespół staje się zbyt duży, warto rozważyć podział na kilka spójnych Scrum Teamów skupionych na tym samym produkcie i mających wspólny cel, Product Backlog oraz Product Ownera.

Enter a query (or 'done' to finish): Jak duży powinien być zespół w Agile? 
W metodologii Agile nie ma jednoznacznej, sztywnej wielkości zespołu, ale zazwyczaj zaleca się, aby był on na tyle mały, aby zapewnić efektywną komunikację i współpracę. Optymalna liczba to zwykle od 3 do 9 osób, co pozwala na skuteczne samoorganizowanie się i szybkie podejmowanie decyzji.

Enter a query (or 'done' to finish): Jakie jest zadanie Scrum Master'a?    
Scrum Master jest odpowiedzialny za zapewnienie, aby Scrum był stosowany zgodnie z opisem w przewodniku. Pomaga wszystkim w zrozumieniu teorii i praktyki Scrum, wspiera efektywność zespołu, tworzy odpowiednie warunki do poprawy praktyk, usuwa przyczyny ograniczające postępy zespołu, dba o przebieg wydarzeń Scrum, instruuje członków zespołu na temat samozarządzania i interdyscyplinarności, pomaga skupić się na tworzeniu wartościowych Incrementów, wspiera Product Ownera w zarządzaniu Product Backlogiem, a także wspiera organizację w wdrażaniu Scrum i usuwa bariery między interesariuszami a zespołem.

Enter a query (or 'done' to finish): done
```

# Load data into GraphRAG system
```bash
(venv) >python -m app.g_loader
```

# Ask Grap RAG
```text
(venv) >python -m app.q_query
Query: Czym różni się Agile od Scrum'a?
Answer: Agile to szeroka filozofia i metodyka zarządzania projektami, oparta na wartościach takich jak elastyczność, współpraca, iteracyjny rozwój i szybkie dostarczanie wartości. Scrum jest jednym z najbardziej popularnych frameworków realizujących zasady Agile, zawierającym określone role (np. Product Owner, Scrum Team), ceremonie (np. Sprint, Daily Scrum) oraz artefakty (np. Product Backlog, Sprint Backlog). Scrum opisany jest w "Przewodniku po Scrumie" i służy praktycznemu wdrażaniu zasad Agile w projektach.

Query: Co to jest Agile?
Answer: Agile to elastyczne i iteracyjne podejście do zarządzania projektami i rozwoju oprogramowania, które koncentruje się na szybkim dostarczaniu wartości, współpracy zespołowej oraz ciągłym doskonaleniu. Metodyka ta opiera się na krótkich cyklach pracy zwanych sprintami, podczas których realizowane są wybrane zadania z backlogu produktu, zarządzanego przez zespół Scrum i Product Ownera. Agile kładzie nacisk na adaptacyjność, minimalizację marnotrawstwa oraz szybkie reagowanie na zmiany, co pozwala na efektywne osiąganie celów projektowych i dostosowywanie się do potrzeb klienta.

Query: Co to jest Sprint?
Answer: Sprint to krótkie, iteracyjne cykle pracy w metodologii Scrum, podczas których zespół realizuje wybrane zadania z Backlogu Produktu, dążąc do osiągnięcia określonego celu Sprintu (Sprint Goal). W trakcie Sprintu zespół planuje, realizuje zadania, codziennie spotyka się na Daily Scrum, a na końcu prezentuje wyniki podczas Sprint Review. Celem Sprintu jest dostarczenie działającego, wartościowego przyrostu produktu, który można ocenić i udoskonalić w kolejnych etapach. Sprint stanowi podstawową jednostkę czasu w Scrumie, umożliwiając efektywne zarządzanie projektem i uczenie się poprzez doświadczenie.

Query: Jak duży powinien być zespół w Scrum?
Answer: Zgodnie z "Przewodnikiem po Scrumie" (Scrum Guide) oraz najlepszymi praktykami, zespół Scrumowy powinien być mały i zwinny, zwykle składający się od 3 do 9 członków. Taki rozmiar umożliwia efektywną komunikację, współpracę, szybkie podejmowanie decyzji oraz skuteczne realizowanie celów Sprintu.

Query: Jak duży powinien być zespół w Agile?
Answer: W Agile, szczególnie w Scrum, zaleca się, aby zespół składał się z około 3 do 9 osób. Taki rozmiar umożliwia efektywną komunikację, szybkie podejmowanie decyzji oraz elastyczność w realizacji zadań i Sprintów. Małe zespoły sprzyjają sprawnej współpracy i skutecznemu dostarczaniu wartości, jednocześnie pozwalając na skuteczne zarządzanie i koordynację.

Query: Jakie jest zadanie Scrum Master'a?
Answer: Zadaniem Scrum Master'a jest wspieranie zespołu Scrum w przestrzeganiu zasad i praktyk Scrum, usuwanie przeszkód, ułatwianie współpracy oraz zapewnienie, że proces Scrum jest realizowany zgodnie z wytycznymi "Przewodnika po Scrumie". Działa jako mentor i facilitator, pomagając zespołowi w realizacji celów Sprintu, promując efektywną współpracę i ciągłe doskonalenie procesu. Scrum Master nie zarządza bezpośrednio Product Backlogiem ani nie wyznacza celów Sprintu, lecz wspiera zespół w ich osiąganiu, dbając o skuteczne stosowanie metodologii Scrum i promowanie zasad zwinności.

Query: Jakie jest zadanie Product Owner'a?
Answer: Zadaniem Product Owner'a jest zarządzanie backlogiem produktu, ustalanie priorytetów oraz określanie wymagań i celów projektu. Odpowiada za tworzenie i utrzymanie elastycznych, dostosowujących się do zmian wymagań produktu, a także za przeprowadzanie analizy tych wymagań. Współpracuje z zespołem Scrum, proponuje ulepszenia produktu, definiuje cele sprintów, nadzoruje planowanie sprintów i zapewnia, że zespół pracuje nad najważniejszymi funkcjami, aby dostarczyć funkcjonalne oprogramowanie dla użytkowników. Jego głównym celem jest priorytetyzacja rozwoju i wdrożenia działającego produktu, aby skutecznie realizować cele projektu.
```

## Performance
```text
GRAPH build communities time: 58sec[33 communities]
GRAPH response time: 20sec[33 communities]
```

# Documentation
```text
Chunking
https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_double_merging_chunking/
https://bitpeak.pl/chunking-methods-in-rag-methods-comparison/
https://medium.com/@sayantanmanna840/rag-chunking-strategies-with-llamaindex-optimizing-your-retrieval-pipeline-6fdb9f0d50c2

ES
https://docs.llamaindex.ai/en/stable/examples/vector_stores/Elasticsearch_demo/
https://docs.llamaindex.ai/en/stable/examples/vector_stores/ElasticsearchIndexDemo/

Metadata
https://docs.llamaindex.ai/en/stable/examples/cookbooks/oreilly_course_cookbooks/Module-4/Metadata_Extraction/

Fusion Retriever
https://docs.llamaindex.ai/en/stable/examples/retrievers/simple_fusion/

GraphRag
https://docs.llamaindex.ai/en/stable/examples/cookbooks/GraphRAG_v2/
```
