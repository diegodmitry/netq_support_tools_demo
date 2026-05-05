# NETQ Support Tools

## Handoff rapido para outra maquina com IA

Se este repositorio for aberto noutra maquina para continuidade com IA, a melhor ordem de leitura e:

1. este `README.md` para contexto geral, arquitetura, setup e fluxo de trabalho
2. `tasks.md` para estado real do backlog, entregaveis e progresso
3. `netq-log-platform/docs/parity-matrix.md` para entender o que ainda precisa atingir paridade com o legado
4. `netq-log-platform/docs/auth-authorization-session-audit-strategy.md` para a estrategia alvo de autenticacao, sessao e controlo de acesso
5. `SECURITY_REPORT.md` para riscos conhecidos e prioridades de hardening

## Estado atual para handoff

Resumo pratico do estado do projeto no momento desta versao do repositorio:

- o legado `NetQTools` continua a ser a referencia funcional principal
- a nova plataforma `netq-log-platform` ja tem base de backend e frontend implementada
- autenticacao, bootstrap de sessao, keep-alive e logout ja foram trabalhados na nova stack
- o modulo `Audit Logs` ainda nao esta fechado ponta a ponta com paridade completa
- o modulo `SIGRA` ainda nao esta fechado ponta a ponta na nova stack
- a parte de containerizacao e rollout em Kubernetes ainda precisa de consolidacao
- existe analise de seguranca produzida em `SECURITY_REPORT.md` e ela deve ser considerada antes de qualquer exposicao maior do sistema

## Proximas prioridades recomendadas

Se a continuidade do trabalho for feita por outra maquina ou por outra IA, a ordem recomendada e:

1. tratar os achados criticos e altos de `SECURITY_REPORT.md`
2. fechar autenticacao/autorizacao no backend da nova plataforma de forma obrigatoria nas rotas de negocio
3. concluir paridade funcional do modulo `Audit Logs`
4. concluir paridade funcional do modulo `SIGRA`
5. reforcar testes automatizados e evidencias de comparacao com o legado
6. finalizar containerizacao, configuracao externa e deploy em Kubernetes

## Riscos conhecidos antes de continuar

Antes de qualquer novo desenvolvimento, vale assumir explicitamente que:

- o repositorio contem material sensivel e precisa de saneamento antes de qualquer publicacao externa
- o legado concentra riscos relevantes de seguranca e nao deve ser usado como referencia de implementacao sem revisao critica
- a plataforma nova ainda tem lacunas de seguranca e de paridade funcional
- arquivos de credenciais, cookies e configuracoes reais nao devem ser replicados para novos repositorios ou ambientes sem limpeza previa

Referencia principal:

- `SECURITY_REPORT.md`

## Visao geral

`NETQ Support Tools` centraliza a modernizacao de uma ferramenta operacional usada para consulta de pedidos, logs e integracoes de suporte.

O repositorio contem:

- o sistema legado `NetQTools`, implementado em Java/JSP
- a nova plataforma `netq-log-platform`, em migracao para Python + FastAPI no backend e Next.js no frontend
- documentacao funcional, tecnica e de infraestrutura para garantir paridade entre legado e nova solucao

## Por que este projeto foi criado

O projeto nasceu para eliminar dependencias operacionais manuais, reduzir tempo de analise e preparar a aplicacao para uma arquitetura mais moderna, segura e facil de manter.

Antes da nova plataforma, parte relevante da analise operacional exigia um fluxo manual no Audit Logs:

1. localizar o registo usando o `ID`
2. selecionar todo o conteudo
3. copiar o payload
4. colar no Notepad++
5. escolher manualmente a linguagem
6. aplicar formatacao com `Pretty Print`

Esse processo gera desperdicio de tempo, aumenta o risco de erro humano e dificulta a leitura rapida de XML/JSON durante troubleshooting.

## Problemas que o projeto resolve

- reduz a dependencia de ferramentas externas para leitura de payloads
- elimina etapas manuais repetitivas no fluxo de analise de Audit Logs
- melhora a legibilidade de requests e responses tecnicos
- centraliza autenticacao, sessao e consultas operacionais numa interface web moderna
- prepara o sistema para deploy padronizado em containers e Kubernetes
- diminui acoplamento do legado com Tomcat, JSP, configuracoes locais e comportamento implicito
- cria base para testes, observabilidade e evolucao segura da aplicacao

## Objetivo da migracao

Reescrever integralmente a aplicacao legada preservando o comportamento funcional critico, mas substituindo a stack atual por uma arquitetura mais clara e sustentavel.

Objetivos principais:

- manter paridade funcional para autenticacao, sessao e modulos operacionais
- expor contratos explicitos de API em vez de HTML gerado dinamicamente no backend
- modernizar a experiencia de uso sem perder regras de negocio existentes
- externalizar configuracoes e segredos
- empacotar frontend e backend em imagens Docker
- executar a solucao em Kubernetes com configuracao apropriada para ambiente corporativo

## Estrutura do repositorio

```text
.
|-- NetQTools/             # aplicacao legada em Java/JSP
|-- netq-log-platform/     # nova plataforma em Python + Next.js
|   |-- backend/           # API FastAPI
|   |-- frontend/          # interface Next.js
|   |-- k8s/               # manifests base de Kubernetes
|   `-- docs/              # catalogos, estrategia e criterios de migracao
|-- screenshots/           # evidencias visuais do fluxo atual
`-- tasks.md               # plano de migracao e inventario tecnico
```

## Onde comecar, dependendo do objetivo

### Se o objetivo for continuar a migracao funcional

- comecar por `tasks.md`
- depois ler `netq-log-platform/docs/parity-matrix.md`
- usar `NetQTools/` como referencia de comportamento do legado
- implementar primeiro no backend `netq-log-platform/backend`, depois ajustar o frontend `netq-log-platform/frontend`

### Se o objetivo for seguranca e hardening

- comecar por `SECURITY_REPORT.md`
- revisar primeiro:
  - `NetQTools/conf/`
  - `NetQTools/src/java/NetqTools/`
  - `netq-log-platform/backend/app/api/`
  - `netq-log-platform/backend/app/application/`
  - `netq-log-platform/backend/app/core/`
  - `netq-log-platform/k8s/base/`

### Se o objetivo for continuidade operacional em outra maquina

- confirmar pre-requisitos locais
- preparar primeiro o backend
- depois preparar o frontend
- validar autenticacao e sessao
- so depois avancar para `Audit Logs`, `SIGRA` e deploy

## Tecnologias usadas e por que foram escolhidas

### Desenvolvimento

#### Legado

- `Java 8`
  Motivo: stack original da aplicacao e base do comportamento que precisa ser preservado.
- `Servlets + JSP`
  Motivo: implementacao atual da autenticacao, navegacao e renderizacao server-side.
- `jQuery + Foundation + DataTables`
  Motivo: composicao atual da interface do utilizador no legado.
- `LDAP SDK`, `HttpClient`, `SOAP API`, `Log4j`
  Motivo: autenticacao corporativa, integracoes HTTP/SOAP e logging operacional.

#### Nova plataforma

- `Python 3.11`
  Motivo: produtividade, clareza de codigo e boa adequacao para servicos backend e integracoes.
- `FastAPI`
  Motivo: contratos de API explicitos, validacao forte, boa ergonomia para testes e estrutura limpa em camadas.
- `ldap3`
  Motivo: integracao com LDAP de forma desacoplada do restante backend.
- `httpx`
  Motivo: cliente HTTP moderno para integrar Audit Logs, SAPA e outras dependencias externas.
- `Next.js 16`
  Motivo: base moderna para a UI, protecao de rotas, rendering hibrido e boa experiencia para aplicacoes internas.
- `React 19`
  Motivo: composicao de interface reutilizavel e evolucao da UX sem depender de manipulacao manual de DOM.
- `TypeScript`
  Motivo: tipagem forte no frontend, menor risco de regressao e melhor manutencao.
- `Vitest`
  Motivo: testes rapidos no frontend, especialmente para comportamento de componentes e utilitarios.
- `Pytest`
  Motivo: suite simples e robusta para testes de backend e contrato de API.
- `Ruff`, `ESLint`, `Prettier`
  Motivo: padronizacao de codigo, consistencia entre equipas e menor custo de revisao.

### Infraestrutura

- `Docker`
  Motivo: empacotamento reproduzivel do backend e frontend, reduzindo variacoes entre ambientes.
- `Kubernetes`
  Motivo: execucao padronizada em ambiente corporativo com escalabilidade, probes e configuracao externa.
- `ConfigMaps`
  Motivo: separar configuracoes nao sensiveis da imagem da aplicacao.
- `Secrets`
  Motivo: proteger credenciais e valores sensiveis, como dados de LDAP e integracoes.
- `Ingress`
  Motivo: publicacao controlada do frontend no cluster.
- `Service`
  Motivo: exposicao estavel dos componentes internos no cluster.
- `Redis` (decisao prevista para producao)
  Motivo: store de sessao compartilhado, evitando perda de sessao em restart de pod e suportando multiplas replicas.

## Arquitetura alvo

- `frontend` Next.js exposto ao utilizador final
- `backend` FastAPI servindo APIs versionadas em `/api/v1`
- autenticacao corporativa via LDAP
- sessao server-side com cookie `HttpOnly`
- integracoes dedicadas para Audit Logs, SAPA e SIGRA
- deploy em Kubernetes com um pod contendo dois containers:
  - frontend na porta `3000`
  - backend na porta `8000`

## Publico-alvo

Este projeto é direcionado principalmente para:

- equipas de suporte operacional que precisam consultar logs, requests e respostas por identificador
- equipas de troubleshooting e analise tecnica que investigam falhas entre sistemas
- equipas de desenvolvimento e manutencao responsaveis pela migracao do legado
- equipas de infraestrutura e plataforma que vao empacotar, publicar e operar a solucao em Kubernetes

## Fluxo de implementacao

O fluxo recomendado de trabalho para este projeto e:

1. mapear no legado o comportamento funcional que precisa ser preservado
2. transformar regras implicitas em contratos explicitos de API e criterios de aceite
3. implementar ou ajustar o backend FastAPI por camadas:
   - `domain`
   - `application`
   - `infrastructure`
   - `api`
4. implementar o frontend Next.js consumindo apenas os contratos novos do backend
5. validar paridade funcional com apoio da documentacao, screenshots e evidencias do legado
6. executar verificacoes locais de qualidade e testes
7. gerar imagens Docker versionadas para backend e frontend
8. publicar as imagens no registry corporativo
9. configurar `ConfigMaps`, `Secrets`, `Service`, `Ingress` e `Deployment`
10. aplicar os manifests no cluster Kubernetes
11. executar smoke tests no pod e validar comportamento funcional apos deploy

### Pipeline pratico sugerido

#### 1. Descoberta e analise

- usar `NetQTools/` como referencia funcional
- usar `tasks.md` e `netq-log-platform/docs/` como fonte de requisitos e contratos
- identificar se a mudanca impacta autenticacao, Audit Logs, SAPA, SIGRA ou sessao

#### 2. Implementacao local

- backend em `netq-log-platform/backend`
- frontend em `netq-log-platform/frontend`
- configuracao por variaveis `NETQ_*`

#### 3. Validacao de qualidade

Na raiz de `netq-log-platform`:

```bash
make quality
make test
```

Isso executa:

- backend: `ruff check .`, `ruff format --check .`, `pytest`
- frontend: `npm run lint`, `npm run format:check`, `npm run typecheck`, `npm run test`

#### 4. Containerizacao

Build das imagens:

```bash
cd netq-log-platform/backend
docker build -t netq-log-platform-backend:local .

cd ../frontend
docker build -t netq-log-platform-frontend:local .
```

#### 5. Publicacao e deploy

Os manifests base estao em `netq-log-platform/k8s/base` e assumem:

- uma imagem de backend
- uma imagem de frontend
- um `Deployment` com dois containers no mesmo pod
- um `Service` expondo o frontend
- um `Ingress` para acesso web

Fluxo esperado de distribuicao das imagens:

1. fazer build local das imagens
2. versionar as tags
3. autenticar no registry
4. fazer push para o registry corporativo ou Docker Hub, conforme o ambiente
5. atualizar os manifests com a tag publicada
6. aplicar os manifests com `kubectl`
7. deixar o cluster fazer o pull das imagens nos nodes que executam os pods

Exemplo generico com registry:

```bash
docker tag netq-log-platform-backend:local <registry>/netq-log-platform-backend:<tag>
docker tag netq-log-platform-frontend:local <registry>/netq-log-platform-frontend:<tag>

docker push <registry>/netq-log-platform-backend:<tag>
docker push <registry>/netq-log-platform-frontend:<tag>
```

Importante:

- o `kubectl` nao faz download da imagem para a maquina do utilizador
- o `kubectl` envia a definicao dos recursos para a API do cluster
- depois disso, os nodes do Kubernetes fazem `pull` das imagens a partir do registry configurado
- por isso, o servidor ou cluster precisa ter acesso de rede ao registry e permissao para fazer `pull`

Aplicacao base:

```bash
kubectl apply -k netq-log-platform/k8s/base
```

Antes de promover para ambientes reais, e necessario:

- substituir valores placeholder em `backend-secret.yaml`
- trocar tags `latest` por tags imutaveis
- rever hostnames e rotas do `Ingress`
- configurar credenciais, URLs e certificados corporativos
- validar comunicacao LDAP e integracoes externas

## Setup local e execucao ponta a ponta

### Pre-requisitos

- `Python 3.11+`
- `Node.js 20+`
- `npm`
- `Docker` para testes de containerizacao
- `kubectl` para deploy em Kubernetes

### 1. Preparar o backend

```bash
cd /Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Configurar ambiente:

```bash
cp /Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend/.env.example .env
```

Observacoes:

- o backend le variaveis com prefixo `NETQ_`
- por omissao, usa `.env`
- para desenvolvimento, existe suporte a `auth_provider=mock`
- valores sensiveis podem ser fornecidos por ficheiros via variaveis como `NETQ_LDAP_USER_DB_PASSWORD_FILE`

Executar backend:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Preparar o frontend

```bash
cd /Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/frontend
npm install
```

Se necessario, exportar a URL da API:

```bash
export NETQ_API_BASE_URL=http://localhost:8000/api/v1
```

Executar frontend:

```bash
npm run dev
```

### 3. Execucao ponta a ponta em modo local

Com backend e frontend ativos:

- frontend: `http://localhost:3000`
- backend: `http://localhost:8000`

Fluxo esperado:

1. abrir `/login`
2. autenticar
3. entrar em `/app`
4. validar bootstrap de sessao
5. executar consultas suportadas
6. verificar keep-alive e logout

### 4. Modo mock para acelerar desenvolvimento

O frontend suporta um modo util para desenvolvimento da UI:

```bash
cd /Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/frontend
NETQ_SKIP_AUTH=true NETQ_USE_MOCKS=true npm run dev
```

Nesse modo:

- o login e ignorado
- `/app` abre diretamente
- consultas `NETQ` usam fixtures/mock local
- fluxos fora de `NETQ` continuam a depender do backend configurado

### 5. Validacao local recomendada

Na raiz de `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform`:

```bash
make quality
make test
```

## Regras importantes para continuidade com IA

- nao assumir que o legado esta seguro so porque esta em producao
- nao copiar credenciais reais para novos arquivos de configuracao
- nao publicar este repositorio sem saneamento previo
- preservar evidencias, backlog e documentacao de decisao durante a continuidade
- sempre comparar comportamento novo com o legado antes de declarar paridade

## Checklist de arranque para outra maquina

1. ler este `README.md`
2. ler `tasks.md`
3. ler `SECURITY_REPORT.md`
4. validar pre-requisitos locais
5. subir backend
6. subir frontend
7. testar login, sessao, keep-alive e logout
8. retomar a partir das prioridades abertas em `tasks.md`
