# Task List — Migração Completa para Python + Next.js

## Nome do projeto
- [x] Nome do novo projeto definido: `netq-log-platform`

## Objetivo
Reescrever integralmente a aplicação legada Java/JSP para uma nova stack com Python + FastAPI no backend e Next.js no frontend, preservando todas as funcionalidades existentes, aplicando clean code, gerando imagem container e executando em pod no Kubernetes.

## Entregáveis
- [ ] Backend FastAPI com paridade funcional do legado.
- [ ] Frontend Next.js com design inspirado na Vercel e paridade funcional da UI atual.
- [ ] Imagens Docker versionadas para backend e frontend.
- [ ] Manifestos Kubernetes ou Helm chart para deploy em pod.
- [ ] Suite de testes de regressão, integração e smoke tests.
- [ ] Documentação técnica, operacional e de rollout.

## Metas mensuráveis
- [ ] Catálogo funcional completo aprovado antes da reescrita.
- [ ] 100% dos fluxos críticos mapeados com critérios de aceite.
- [ ] Paridade validada para autenticação, navegação, consultas e integrações externas.
- [ ] Deploy via container executando localmente e em ambiente Kubernetes.
- [ ] Observabilidade, probes e configuração externa prontas antes do go-live.

## Estado atual resumido

- [x] Legado inventariado e fluxos principais mapeados.
- [x] Backend FastAPI base implementado com health, readiness, métricas, logging e configuração por ambiente.
- [x] Frontend Next.js base implementado com shell autenticada, middleware e componentes reutilizáveis.
- [x] Pipeline local pronta com `make quality` e `make test`.
- [x] Autenticação e sessão validadas em ambiente real via LDAP:
  login, bootstrap de sessão, keep-alive, logout e rejeição pós-logout.
- [ ] Audit Logs ainda não implementado ponta a ponta no novo stack.
- [ ] SIGRA ainda não implementado ponta a ponta no novo stack.
- [ ] Containerização e Kubernetes ainda pendentes.

## Itens em andamento

- [ ] Corrigir a formatação de payloads XML embutidos em `requestPayload` e `responsePayload` no Audit Logs da nova aplicação, preservando também a legibilidade de blocos textuais como `<log>`.
- [x] Implementar visualização em árvore no `CodeViewer` para payloads XML.
- [x] Garantir que nós XML com filhos tenham chevron para expand/collapse.
- [x] Garantir que o payload XML abra totalmente expandido por padrão após `Submit`.
- [x] Exibir nó colapsado em linha resumida no formato `<tag>...</tag>`.
- [x] Implementar seleção visual de nó no `CodeViewer`.
- [x] Exibir linha vertical ativa ao lado do nó XML selecionado.
- [x] Garantir que apenas um nó fique selecionado por instância do `CodeViewer`.
- [x] Aplicar a árvore XML a todos os usos de `CodeViewer` com `language="xml"`.
- [x] Preservar comportamento atual para conteúdos não XML no `CodeViewer`.
- [x] Preservar ações atuais de `Copy`, zoom e scroll horizontal no modo árvore.
- [x] Refatorar a implementação com clean code: parser XML, helpers e renderização separados.
- [x] Criar tipos explícitos para nós XML e ids estáveis para expansão/seleção.
- [x] Remover dependência de `dangerouslySetInnerHTML` no modo árvore XML.
- [x] Garantir acessibilidade com `button`, `aria-expanded` e estado de seleção.
- [ ] Adicionar testes para parsing de XML, colapso, expansão e seleção visual.
- [ ] Ajustar o setup de testes para DOM/`jsdom` se necessário para testar o `CodeViewer`.
- [x] Validar a implementação com `npm run test`, `npm run typecheck` e `npm run lint`.

## Plano atual — Kubernetes com pod único e dois containers

- [ ] Containerizar o backend FastAPI em imagem própria para execução com `uvicorn` na porta `8000`.
- [ ] Containerizar o frontend Next.js em imagem própria para execução com `next start` na porta `3000`.
- [ ] Adotar nomes iniciais das imagens:
  backend `ossm-docker-registry.telecom.pt:5000/netq-log-platform-backend:<tag>`
  e frontend `ossm-docker-registry.telecom.pt:5000/netq-log-platform-frontend:<tag>`.
- [ ] Publicar ambas as imagens no registry interno corporativo.
- [ ] Criar `Deployment` com um pod contendo dois containers:
  frontend + backend.
- [ ] Configurar o frontend para chamar o backend no mesmo pod via `NETQ_API_BASE_URL=http://127.0.0.1:8000/api/v1`.
- [ ] Criar `ConfigMap` próprio do projeto para configuração não sensível do pod.
- [ ] Criar `Secret` próprio do projeto, separado dos segredos já existentes, para credenciais e valores sensíveis.
- [ ] Manter a imagem do backend com conjunto mínimo de troubleshooting:
  `curl`, `openssl` e `ca-certificates`.
- [ ] Injetar `NETQ_LDAP_SERVER=ldap.example.internal` e `NETQ_LDAP_USE_SSL=true` no backend do pod real.
- [ ] Validar se a confiança TLS da CA corporativa precisa ser adicionada ao container do backend para LDAP.
- [ ] Expor somente o frontend por `Service`.
- [ ] Publicar o acesso web por `Ingress`/NGINX apontando para o `Service` do frontend.
- [ ] Executar smoke tests no pod real:
  `/health`, `/ready`, `/api/v1/auth/config`, `/api/v1/auth/login` e `/api/v1/audit-logs/query`.
- [ ] Abrir ação separada para definir o valor final operacional de `NETQ_LDAP_SERVER`.

## Backlog — Próxima versão

- [ ] Adicionar line numbers no `CodeViewer` com gutter dedicado, compatível com modo simples e árvore XML.
- [ ] Garantir que a numeração acompanhe apenas linhas visíveis no modo árvore, recalculando após expand/collapse.
- [ ] Manter `Copy` e `Copy All` copiando apenas o payload, sem incluir os números de linha.
- [ ] Preservar alinhamento entre line numbers, chevrons, indentação da árvore e guide column.
- [ ] Garantir acessibilidade do gutter de line numbers sem poluir leitura por screen readers.

## Fase 1 — Acesso e Descoberta (Semana 1–2)
[x] Obter checkout do SVN (URL + credenciais).
[x] Identificar stack Java/JS, build e runtime.
[ ] Mapear integrações críticas (banco, APIs, filas, arquivos).
[ ] Levantar fluxos críticos e top 3–5 incidentes.

## Inventário técnico atual

### Stack atual e funções

| Área | Tecnologia atual | Função no sistema | Evidência |
|---|---|---|---|
| Backend | Java 8 | Lógica principal da aplicação | `NetQTools/nbproject/project.properties` |
| Backend web | Servlet/JSP | Processa requests, autenticação, renderização inicial | `NetQTools/web/WEB-INF/web.xml` |
| Container/runtime | Apache Tomcat 9 | Executa o WAR web | `NetQTools/nbproject/private/private.properties` |
| Build backend | Ant + NetBeans | Compila, empacota e faz deploy | `NetQTools/build.xml` |
| Artifact | WAR | Pacote de deploy da aplicação | `NetQTools/nbproject/project.properties` |
| Frontend | JSP | Páginas server-side | `NetQTools/web/index.jsp` |
| Frontend JS | jQuery 3.2.1 | DOM, AJAX e interações de tela | `NetQTools/web/js/vendor/jquery.js` |
| Frontend UI | Foundation | Layout e componentes visuais | `NetQTools/web/jsInclude.jsp` |
| Tabela UI | DataTables 1.10.16 | Tabelas e navegação de dados | `NetQTools/web/js/jquery.dataTables.min.js` |
| UX feedback | SweetAlert2 | Alerts e loading visual | `NetQTools/web/js/app.js` |
| Syntax/UI | Highlight.js | Exibição formatada de payloads XML/JSON | `NetQTools/web/jsInclude.jsp` |
| Configuração | JSON externo em `catalina.base/conf/NetQTools` | URLs, LDAP, SIGRA, logs | `NetQTools/src/java/NetqTools/Login.java` |
| Logging | Log4j2 | Logs da aplicação | `NetQTools/conf/log4j.xml` |
| Auth | LDAP via UnboundID | Login corporativo | `NetQTools/src/java/NetqTools/Login.java` |
| Integração HTTP | HttpClient/Commons/HtmlUnit | Consultas a sistemas externos | `NetQTools/src/java/NetqTools/URLRequest.java` |
| Integração SOAP | `javax.xml.soap` | Chamada ao SIGRA/TIBCO | `NetQTools/src/java/NetqTools/URLRequestSigra.java` |

### Endpoints e runtime

| Componente | Endpoint/contexto | Função |
|---|---|---|
| Contexto web | `/NetqTools` | Context path da aplicação no Tomcat |
| Welcome page | `index.jsp` | Tela inicial de login |
| Login servlet | `/login.do` | Autenticação do utilizador |
| Logout servlet | `/logout.do` | Encerramento de sessão |
| SessionPing servlet | `/doPing.do` | Manutenção/validação de sessão |
| URLRequest servlet | `/URLRequest` | Consultas a sistemas e montagem das respostas HTML |
| URLRequestSigra servlet | `/URLRequestSigra` | Chamada SOAP ao SIGRA/TIBCO |

### Dependências Java identificadas

| Categoria | Dependências principais | Função |
|---|---|---|
| JSON | Gson 2.8.2 | Leitura e parsing de configuração/respostas |
| Logging | Log4j2 2.24.3 | Logging da aplicação |
| Utilitários | Commons Codec/IO/Lang/Text/Net | Suporte a encoding, IO, strings e rede |
| HTTP | Apache HttpClient/HttpCore/HttpMime | Chamadas HTTP externas |
| HTML/browser | HtmlUnit 2.60.0 + Jetty/WebSocket | Automação/manipulação de conteúdo remoto |
| Diretório | UnboundID LDAP SDK 7.0.2 | Autenticação LDAP |
| UI server-side | JSTL 1.2.5 | Apoio a JSP |
| SOAP | `javax.xml.soap-api` 1.4.0 | Integração SIGRA/TIBCO |
| Codegen | Lombok 1.18.36 | Redução de boilerplate |

### Stack alvo decidida

| Camada | Tecnologia | Diretriz |
|---|---|---|
| Backend | Python + FastAPI | APIs, autenticação, integrações, regras de negócio, observabilidade |
| Frontend | Next.js | UI web moderna com design inspirado na Vercel |
| Qualidade | Clean Code | Baixo acoplamento, alta coesão, nomes claros, testes, separação por camadas |
| Empacotamento | Docker | Imagens reproduzíveis para backend e frontend |
| Orquestração | Kubernetes | Execução em pod com probes, config externa e escalabilidade |
| Configuração | Env vars + Secrets + ConfigMaps | Remover segredos hardcoded e externalizar ambientes |

## Princípios de implementação

- [x] Aplicar clean code desde o início: domínio, aplicação, infraestrutura e interface separados.
- [x] Evitar portar bugs implícitos sem antes documentá-los como comportamento legado.
- [x] Não reimplementar UI antes de fechar contrato funcional do backend.
- [ ] Toda funcionalidade migrada precisa de critério de aceite, caso de teste e evidência de comparação com o legado.
- [ ] Não carregar credenciais no repositório.
- [ ] Priorizar compatibilidade funcional antes de otimização ou redesign profundo.

## Mapeamento funcional inicial

| Fluxo | Origem atual | Função | Observação de migração |
|---|---|---|---|
| Login | `index.jsp` + `Login.java` | Autenticação LDAP e criação de sessão | Deve migrar para autenticação backend Python com sessão/token e proteção de rotas |
| Logout | `Logout.java` | Encerrar sessão | Deve invalidar sessão/token e limpar estado do frontend |
| Keep-alive | `SessionPing.java` + `menu.jsp` | Manter sessão viva | Deve ter equivalente com estratégia explícita de sessão no novo frontend |
| Menu principal | `menu.jsp` | Navegação para módulos Audit Logs e SIGRA | Deve virar layout/app shell Next.js |
| Consulta Audit Logs | `netqLogs.jsp` + `URLRequest.java` | Consultar pedidos por ambiente, tipo e ID | Deve migrar para API JSON + renderização React/Next |
| Consulta SAPA | `netqLogs.jsp` + `URLRequest.java` | Consultar por SAPA ID | Deve permanecer como fluxo independente dentro do módulo Audit Logs |
| Expansão de registos | `app.js` + `URLRequest.java` | Abrir detalhes left/right e pedidos relacionados | Fluxo sensível de paridade; precisa de contrato de resposta claro |
| Consulta SIGRA | `sigra.jsp` + `URLRequestSigra.java` | Validar AC e consultar SIGRA/TIBCO via SOAP | Deve manter validação de input, request SOAP e exibição de request/response |
| Renderização de payload | `highlight.pack.js` | Mostrar XML/JSON formatado | Pode usar componente de code viewer moderno mantendo legibilidade |

## Riscos de paridade funcional

| Risco | Impacto | Probabilidade | Mitigação |
|---|---|---|---|
| Regras escondidas nos servlets/JSPs | Alto | Alto | Mapear comportamento por fluxo, parâmetros, redirects, timeouts e mensagens antes da reescrita |
| HTML gerado dinamicamente no backend atual | Alto | Alto | Converter para contrato JSON explícito e criar snapshots comparativos entre respostas |
| Diferença de modelo de sessão entre Java servlet e novo stack | Alto | Médio | Definir cedo a estratégia de auth: cookie de sessão segura ou token com refresh controlado |
| Dependência de LDAP corporativo | Alto | Médio | Criar ambiente de teste controlado e mocks para desenvolvimento |
| Integrações HTTP com comportamento não documentado | Alto | Alto | Catalogar URLs, headers, auth, timeout, retries, payloads e respostas esperadas |
| Integração SOAP SIGRA/TIBCO | Alto | Alto | Registrar envelopes SOAP reais, namespaces, timeouts e exemplos de sucesso/erro |
| Dependência de arquivos externos em `catalina.base/conf/NetQTools` | Alto | Alto | Migrar configuração para env vars, Secrets e ConfigMaps com matriz por ambiente |
| Comportamentos de UI baseados em jQuery | Médio | Alto | Levantar todas as interações do `app.js` e reproduzir comportamento no frontend novo |
| Mensagens e redirects implícitos de autenticação | Médio | Médio | Criar critérios de aceite para erro de login, sessão expirada e logout |
| Diferença visual excessiva durante redesign | Médio | Médio | Manter estrutura funcional e hierarquia de navegação antes de refinamentos estéticos |
| Falta de testes no legado | Alto | Alto | Criar harness de regressão com casos capturados do sistema atual |
| Segredos hardcoded no legado | Alto | Alto | Rotacionar segredos, remover do código novo e usar secret store |
| Deploy container sem readiness/liveness corretos | Alto | Médio | Implementar probes, graceful shutdown e startup checks antes de produção |
| Divergência entre ambientes DEV/PRD | Alto | Alto | Criar matriz de configuração e checklist de validação por ambiente |

## Estratégia de paridade funcional

1. Catalogar telas, endpoints, inputs, outputs, mensagens, redirects e integrações atuais.
2. Gravar exemplos reais de requests e responses do legado para cada fluxo crítico.
3. Definir contrato alvo em JSON para cada caso de uso.
4. Implementar backend FastAPI com testes de contrato e mocks de integração.
5. Implementar frontend Next.js consumindo apenas os contratos novos.
6. Executar comparação funcional lado a lado entre legado e novo.
7. Liberar por homologação funcional antes do corte definitivo.

## Contrato alvo JSON — Audit Logs

### Objetivo

- [ ] Substituir a resposta HTML fragmentada do legado por um contrato JSON explícito.
- [ ] Preservar o comportamento funcional atual de `NETQ`, `SAPA` e IDs externos.
- [ ] Separar claramente payload de audit, payload de mongo, tipo do pedido e registos relacionados.

### Endpoint alvo sugerido

- [ ] `POST /api/v1/audit-logs/query`
- [ ] `POST /api/v1/audit-logs/related-detail`

### Request — consulta principal

```json
{
  "environment": "prod",
  "queryType": "NETQ",
  "queryValue": "ORDER_ID_123",
  "source": "request-id"
}
```

### Campos esperados da request principal

- [x] `environment`: `prod` ou `qa`
- [x] `queryType`: `NETQ`, `TIBCO`, `NETWIN`, `SIGRA`, `NA`, `SAPA`
- [x] `queryValue`: identificador submetido pelo utilizador
- [x] `source`: `request-id` ou `sapa-id`

### Regras de mapeamento legado -> novo contrato

- [x] `environment=prod` corresponde ao legado `req=prodMongo`
- [x] `environment=qa` corresponde ao legado `req=qaMongo`
- [x] `queryType=SAPA` ou `source=sapa-id` corresponde ao legado `req=sapa`
- [x] `queryType=NETQ` ativa fluxo combinado audit + mongo + relacionados
- [x] `queryType!=NETQ` ativa fluxo de payload único externo

### Response — consulta principal NETQ

```json
{
  "query": {
    "environment": "prod",
    "queryType": "NETQ",
    "queryValue": "ORDER_ID_123",
    "source": "request-id"
  },
  "mode": "netq",
  "result": {
    "rootOrderId": "ORDER_ID_123",
    "records": [
      {
        "orderId": "ORDER_ID_123",
        "orderType": "ORDER_TYPE",
        "auditPayload": {
          "contentType": "application/xml",
          "formatted": "<xml>...</xml>",
          "raw": "<xml>...</xml>"
        },
        "mongoPayload": {
          "contentType": "application/xml",
          "formatted": "<xml>...</xml>",
          "raw": "<xml>...</xml>"
        },
        "relatedOrderIds": [
          "ORDER_ID_456",
          "ORDER_ID_789"
        ]
      }
    ]
  },
  "meta": {
    "totalRecords": 1,
    "generatedAt": "2026-03-18T12:00:00Z"
  }
}
```

### Response — consulta principal ID externo

```json
{
  "query": {
    "environment": "qa",
    "queryType": "TIBCO",
    "queryValue": "EXT_ID_123",
    "source": "request-id"
  },
  "mode": "external",
  "result": {
    "externalSystem": "TIBCO",
    "externalId": "EXT_ID_123",
    "payload": {
      "contentType": "application/xml",
      "formatted": "<xml>...</xml>",
      "raw": "<xml>...</xml>"
    }
  },
  "meta": {
    "generatedAt": "2026-03-18T12:00:00Z"
  }
}
```

### Response — consulta SAPA

```json
{
  "query": {
    "environment": "prod",
    "queryType": "SAPA",
    "queryValue": "SAPA_123",
    "source": "sapa-id"
  },
  "mode": "sapa",
  "result": {
    "sapaId": "SAPA_123",
    "payload": {
      "contentType": "application/xml",
      "formatted": "<xml>...</xml>",
      "raw": "<xml>...</xml>"
    }
  },
  "meta": {
    "generatedAt": "2026-03-18T12:00:00Z"
  }
}
```

### Request — detalhe relacionado

```json
{
  "environment": "prod",
  "orderId": "ORDER_ID_456",
  "panel": "left"
}
```

### Campos esperados da request de detalhe

- [x] `environment`: `prod` ou `qa`
- [x] `orderId`: id do registo expandido
- [x] `panel`: `left` ou `right`

### Response — detalhe relacionado

```json
{
  "query": {
    "environment": "prod",
    "orderId": "ORDER_ID_456",
    "panel": "left"
  },
  "result": {
    "orderId": "ORDER_ID_456",
    "panel": "left",
    "payload": {
      "contentType": "application/xml",
      "formatted": "<xml>...</xml>",
      "raw": "<xml>...</xml>"
    }
  },
  "meta": {
    "generatedAt": "2026-03-18T12:00:00Z"
  }
}
```

### Regra de paridade para detalhe relacionado

- [x] `panel=left` deve devolver o equivalente ao payload mongo do legado
- [x] `panel=right` deve devolver o equivalente ao payload audit do legado
- [x] O frontend novo não deve depender de posição em lista plana

### Regras de resposta e erro

- [x] Respostas devem ser JSON estável e versionado
- [ ] Timeout de integração deve devolver erro técnico padronizado
- [ ] Resultado vazio deve devolver estrutura válida com indicação de vazio
- [ ] Erro externo deve ser distinguido de erro interno

### Response — erro padronizado

```json
{
  "error": {
    "code": "UPSTREAM_TIMEOUT",
    "message": "Timeout while querying upstream service",
    "details": {
      "system": "mongoProd",
      "queryType": "NETQ"
    }
  },
  "meta": {
    "generatedAt": "2026-03-18T12:00:00Z",
    "requestId": "req-123"
  }
}
```

### Campos mínimos de observabilidade

- [x] `meta.generatedAt`
- [x] `meta.requestId`
- [ ] logs com `environment`, `queryType`, `queryValue` e resultado

### Critérios de aceite do contrato Audit Logs

- [x] O contrato cobre `NETQ`, IDs externos e `SAPA`
- [x] O contrato elimina dependência de HTML gerado no backend
- [x] O contrato elimina dependência de listas planas indexadas
- [x] O contrato separa claramente audit payload e mongo payload
- [x] O contrato suporta expansão de detalhes left/right com semântica explícita

## Ciclo de desenvolvimento recomendado

- [ ] Trabalhar em sprints curtas de 1 a 2 semanas.
- [ ] Executar a migração por módulo funcional, não por camada isolada.
- [ ] Fechar cada sprint com entrega testável ponta a ponta.
- [ ] Exigir validação de paridade funcional ao final de cada módulo.
- [ ] Não iniciar o módulo seguinte sem critérios mínimos de aceite do módulo atual.

### Fluxo padrão de cada sprint

- [ ] Descobrir comportamento atual do módulo no legado.
- [ ] Documentar regras, inputs, outputs, erros e integrações.
- [ ] Definir contrato backend do módulo.
- [ ] Implementar backend FastAPI do módulo.
- [ ] Implementar frontend Next.js do módulo.
- [ ] Executar testes unitários, integração e E2E do módulo.
- [ ] Validar paridade funcional com evidências comparativas.
- [ ] Homologar o módulo antes de avançar.

## Fases de migração

### Fase 1 — Descoberta e especificação funcional

- [x] Inventariar todos os fluxos, entradas, saídas, regras, erros e dependências.
  Evidências/documentação:
  `netq-log-platform/docs/functional-catalog.md`
  `netq-log-platform/docs/integrations.md`
  `netq-log-platform/docs/parity-matrix.md`
  `netq-log-platform/docs/acceptance-criteria.md`
- [x] Mapear integrações: LDAP, HTTP, SOAP, arquivos, logs e ambientes.
- [ ] Capturar evidências do legado: screenshots, requests, responses e mensagens.
  Screenshots já capturados em:
  `screenshots/`
  Índice atual:
  `netq-log-platform/docs/evidence/README.md`
  Nota:
  evidências dos fluxos `SIGRA` e `external-id` ficam adiadas para depois.
- [x] Criar matriz de paridade funcional por módulo.
- [ ] Definir NFRs: segurança, observabilidade, performance, disponibilidade e operação.

### Fase 2 — Arquitetura alvo e fundações

- [x] Definir arquitetura backend em camadas: `domain`, `application`, `infrastructure`, `api`.
- [x] Definir arquitetura frontend: `app`, `features`, `shared/ui`, `shared/lib`.
- [x] Padronizar clean code, lint, formatter, testes e convenções de nomes.
  Referência:
  `netq-log-platform/docs/development-standards.md`
- [x] Definir estratégia de autenticação, autorização, sessão e auditoria.
  Documento:
  `netq-log-platform/docs/auth-authorization-session-audit-strategy.md`
- [x] Executar pipeline de qualidade ponta a ponta no ambiente.
- [x] Definir contratos iniciais das APIs.
- [x] Definir política de atualização de dependências confiáveis e estáveis.
  Documento:
  `netq-log-platform/docs/dependency-update-policy.md`

### Fase 3 — Backend FastAPI base

- [x] Criar projeto FastAPI com health, readiness e versionamento de API.
- [x] Implementar configuração por ambiente usando env vars e secrets.
  Referências:
  `netq-log-platform/backend/.env.example`
  `netq-log-platform/backend/app/core/config.py`
- [x] Implementar logging estruturado, correlação de requests e métricas.
  Referências:
  `netq-log-platform/backend/app/core/observability.py`
  `netq-log-platform/backend/app/main.py`
- [x] Implementar cliente LDAP encapsulado.
  Referências:
  `netq-log-platform/backend/app/infrastructure/auth/ldap_client.py`
  `netq-log-platform/backend/app/infrastructure/auth/gateway.py`
- [x] Implementar clientes HTTP e SOAP com timeout, retry e tratamento de erro.
  Referências:
  `netq-log-platform/backend/app/infrastructure/http/client.py`
  `netq-log-platform/backend/app/infrastructure/sigra/soap_client.py`
- [x] Criar testes unitários e de integração para adaptadores externos.

### Fase 4 — Frontend Next.js base

- [x] Criar app Next.js com TypeScript.
- [x] Definir design system inspirado na Vercel: layout minimalista, tipografia forte, contraste alto, componentes limpos e foco em produtividade operacional.
  Referências:
  `netq-log-platform/docs/design-system.md`
  `netq-log-platform/frontend/app/globals.css`
- [x] Implementar app shell com autenticação e rotas protegidas.
- [x] Criar componentes reutilizáveis para formulários, tabelas, estados de loading, erro e code viewer.
- [x] Garantir responsividade e acessibilidade básica. Mas a aplicação é prioritariamente desktop, então foco em breakpoint maior.

### Fase 5 — Migração do módulo de autenticação

- [x] Migrar login LDAP.
- [x] Reproduzir comportamento de falha de autenticação, sessão e logout.
- [x] Implementar keep-alive ou política de expiração equivalente.
- [x] Validar sessão expirada, credenciais inválidas e utilizador sem permissão.

### Fase 6 — Migração do módulo Audit Logs

- [ ] Migrar consulta por ambiente, tipo de ID e ID.
  Status:
  em progresso; backend, frontend e testes iniciais já implementados
  Subtasks:
  - [x] Implementar endpoint `POST /api/v1/audit-logs/query` no backend.
  - [x] Validar payload de entrada com `environment`, `queryType`, `queryValue` e `source`.
  - [x] Mapear `environment=prod` para upstreams `auditProd` e `mongoProd`.
  - [x] Mapear `environment=qa` para upstreams `auditQA` e `mongoQA`.
  - [x] Mapear `queryType=NETQ` para o fluxo combinado audit + mongo.
  - [x] Mapear `queryType!=NETQ` para o fluxo de ID externo no upstream de audit.
  - [x] Preservar a distinção entre `request-id` e `sapa-id` no contrato novo.
  - [x] Normalizar a resposta do legado para JSON estável no backend.
  - [x] Padronizar tratamento de erro para timeout, upstream indisponível e resultado vazio.
  - [x] Criar testes unitários para regras de roteamento por ambiente e tipo de ID.
  - [x] Criar testes de integração para respostas `NETQ` e `external-id`.
  - [x] Implementar formulário no frontend com seleção de ambiente, tipo de ID e campo de ID.
  - [x] Ligar o frontend ao endpoint novo e renderizar loading, sucesso, vazio e erro.
  - [ ] Validar a consulta principal contra evidências do legado.
- [x] Migrar consulta SAPA.
  Subtasks:
  - [x] Implementar suporte a `source=sapa-id` no backend.
  - [x] Mapear consulta SAPA para o upstream `sapaUrl` do legado.
  - [x] Implementar transformação da resposta SAPA para o modo `sapa` do contrato JSON.
  - [x] Validar diferenças entre consulta SAPA e consulta principal por `request-id`.
  - [x] Criar testes unitários para roteamento do fluxo SAPA.
  - [x] Criar testes de integração para resposta de sucesso, vazio e erro do fluxo SAPA.
  - [x] Implementar entrada SAPA dedicada no frontend ou alternância explícita de fonte.
  - [x] Exibir payload SAPA no frontend usando o mesmo code viewer do módulo.
  - [x] Validar o fluxo SAPA contra evidências do legado.
- [ ] Migrar expansão de registos e pedidos relacionados.
  Subtasks:
  - [x] Implementar endpoint `POST /api/v1/audit-logs/related-detail` no backend.
  - [x] Mapear `panel=left` para o equivalente ao payload mongo do legado.
  - [x] Mapear `panel=right` para o equivalente ao payload audit do legado.
  - [x] Implementar descoberta e retorno estruturado de `relatedOrderIds` no fluxo `NETQ`.
  - [x] Garantir carregamento sob demanda dos detalhes relacionados, sem depender de índices de lista plana.
  - [x] Padronizar resposta JSON para detalhe relacionado com `orderId`, `panel` e `payload`.
  - [x] Criar testes unitários para mapeamento `left/right`.
  - [x] Criar testes de integração para expansão de detalhe e pedidos relacionados.
  - [x] Implementar accordion, expansão ou painel equivalente no frontend novo.
  - [x] Exibir claramente o tipo do pedido e distinguir payload audit vs mongo.
  - [ ] Validar comportamento de expansão e detalhe contra evidências do legado.
- [x] Padronizar resposta do backend em JSON.
- [x] Validar todos os caminhos: sucesso, vazio, timeout, erro externo e payload grande.

### Fase 7 — Migração do módulo SIGRA

- [ ] Migrar validação de AC.
- [ ] Migrar integração SOAP SIGRA/TIBCO.
  Subtasks:
  - [ ] Reproduzir no backend novo a construção do envelope SOAP do legado.
  - [ ] Mapear corretamente `sigraApp`, `sigraCodeApp`, `sigraUrl`, `sigraAction` e `sigraTimeout`.
  - [ ] Implementar cliente SOAP reutilizando o adaptador HTTP do backend.
  - [ ] Preservar geração de campos dinâmicos equivalentes a `npu` e `creationTime`.
  - [ ] Devolver no contrato novo tanto `request_xml` quanto `response_xml`.
  - [ ] Padronizar tratamento de timeout, erro técnico e erro funcional do upstream.
  - [ ] Criar testes unitários para montagem do envelope SOAP.
  - [ ] Criar testes de integração para chamada SOAP com sucesso e falha.
  - [ ] Implementar ação no frontend para submeter AC ao endpoint novo.
  - [ ] Exibir request e response com code viewer no frontend.
  - [ ] Validar request/response do fluxo novo contra evidências do legado.
- [ ] Exibir request e response com code viewer equivalente ao highlight atual.
- [ ] Validar sucesso, erro funcional, timeout e erro técnico.

### Fase 8 — Paridade visual e UX

- [ ] Aplicar visual inspirado na Vercel sem alterar fluxo funcional.
- [ ] Refinar hierarquia visual, navegação, estados vazios e feedback de loading.
- [ ] Garantir consistência entre login, menu, módulos, tabelas e visualização de payload.

### Fase 9 — Containerização

- [ ] Criar Dockerfile do backend.
- [ ] Criar Dockerfile do frontend.
- [ ] Definir estratégia de execução: pods separados frontend/backend ou frontend atrás de ingress consumindo API backend.
- [ ] Externalizar configuração.
- [ ] Validar execução local via containers.

### Fase 10 — Kubernetes

- [ ] Criar manifests ou Helm chart para `Deployment`, `Service`, `Ingress`, `ConfigMap` e `Secret`.
- [ ] Configurar readiness e liveness probes.
- [ ] Configurar requests/limits.
- [ ] Configurar rolling update e rollback.
- [ ] Validar logs, métricas e conectividade com dependências externas.

### Fase 11 — Testes e homologação

- [ ] Testes unitários backend e frontend.
- [ ] Testes de integração com LDAP, HTTP e SOAP.
- [ ] Testes E2E dos fluxos críticos.
- [ ] Testes de regressão de paridade funcional.
- [ ] UAT com checklist baseado no legado.

### Fase 12 — Cutover e estabilização

- [ ] Publicar versão candidata.
- [ ] Executar smoke test pós-deploy.
- [ ] Acompanhar erros, timeouts e comportamento real.
- [ ] Corrigir desvios de paridade rapidamente.
- [ ] Encerrar legado apenas após janela de estabilização aprovada.

## Critérios de aceite por módulo

| Módulo | Critério mínimo de aceite |
|---|---|
| Login | Autentica via LDAP, rejeita inválidos, respeita permissões e mantém sessão conforme política definida |
| Menu | Permite navegar entre os módulos sem regressão de acesso |
| Audit Logs | Consulta todos os tipos suportados e reproduz detalhes/relacionados corretamente |
| SAPA | Consulta por SAPA ID com mesmo comportamento funcional do legado |
| SIGRA | Valida AC, envia SOAP corretamente e mostra request/response |
| Observabilidade | Logs estruturados, métricas e health/readiness ativos |
| Deploy | Imagens sobem em ambiente local e em pod Kubernetes |

## Backlog macro sugerido

- [x] Confirmar stack alvo: FastAPI + Next.js.
- [x] Criar catálogo funcional detalhado do legado.
- [x] Mapear integrações externas e dependências de ambiente.
- [x] Definir arquitetura alvo e padrões clean code.
- [x] Criar backend base com observabilidade e configuração externa.
- [x] Criar frontend base com design system inspirado na Vercel.
- [x] Migrar autenticação.
- [ ] Migrar Audit Logs.
- [ ] Migrar SIGRA.
- [ ] Implementar testes de paridade.
- [ ] Containerizar backend e frontend.
- [ ] Publicar em Kubernetes.
- [ ] Homologar e executar cutover.

## Plano por sprint/módulo

### Sprint 0 — Preparação e alinhamento

- [x] Consolidar inventário técnico e funcional do legado.
- [x] Confirmar critérios de aceite globais da migração.
- [ ] Fechar stack alvo, padrões clean code e convenções de projeto.
- [ ] Definir estratégia de branching, CI, ambientes e revisão técnica.

### Sprint 1 — Descoberta funcional estruturada

- [x] Criar catálogo funcional completo por tela, endpoint e integração.
- [ ] Capturar evidências do legado: requests, responses, mensagens e screenshots.
- [x] Criar matriz de paridade funcional.
- [ ] Identificar gaps, ambiguidades e riscos altos por módulo.

### Sprint 2 — Fundação arquitetural

- [x] Criar estrutura base do backend FastAPI.
- [x] Criar estrutura base do frontend Next.js.
- [x] Configurar lint, formatter, testes e convenções de código.
- [x] Definir contratos iniciais, autenticação, sessão e observabilidade.

### Sprint 3 — Infraestrutura técnica base

- [x] Implementar config por ambiente, secrets e logging estruturado.
- [x] Implementar health, readiness e métricas básicas.
- [x] Implementar clientes base de LDAP, HTTP e SOAP.
- [ ] Preparar ambientes de desenvolvimento e homologação.

### Sprint 4 — Módulo Autenticação

- [x] Documentar comportamento atual de login, logout, sessão e permissões.
- [x] Implementar autenticação LDAP no backend.
- [x] Implementar login/logout e proteção de rotas no frontend.
- [x] Validar sessão expirada, falha de login e utilizador sem permissão.
- [x] Homologar paridade funcional do módulo de autenticação.
  Nota:
  a falha de LDAP real foi rastreada até um override incorreto de `NETQ_LDAP_USER_DN` no `backend/.env`, que sobrepunha o valor válido carregado via `NETQ_LEGACY_CONFIG_FILE`.

## Gate mínimo para iniciar testes úteis

- [x] `make quality` executa localmente sem depender de `ruff` global no `PATH`.
- [x] `make test` executa backend e frontend numa única entrypoint.
- [x] Backend cobre ciclo mínimo de autenticação e sessão:
  login válido, login inválido, utilizador não autorizado, bootstrap de sessão, keep-alive e logout.
- [x] Frontend cobre o gate mínimo de navegação protegida via middleware:
  acesso a `/`, `/login` e `/app`.
- [x] Logout backend devolve limpeza de cookie com headers `no-store` equivalentes ao legado.
- [x] Frontend ignora artefactos gerados em `.next` durante `format:check`.
- [ ] Capturar evidências pendentes de `Audit Logs` e `SIGRA` antes de iniciar testes úteis de paridade ponta a ponta.
- [ ] Implementar os contratos/API dos módulos `Audit Logs` e `SIGRA` antes de iniciar integração funcional além de autenticação.

## Checklist para teste real sem mock

Referência operacional:
`netq-log-platform/docs/real-test-readiness.md`

- [x] Mapear a configuração real já disponível em `NetQTools/conf/app.json`, `app_DEV.json` e `app_PRD.json`.
- [x] Confirmar no legado como essa configuração é usada em `Login.java`, `URLRequest.java` e `URLRequestSigra.java`.
- [x] Permitir ao backend novo carregar configuração real do legado através de `NETQ_LEGACY_CONFIG_FILE`.
- [x] Permitir teste real de autenticação só com LDAP quando `NETQ_ALLOWED_USERS` estiver vazio.
- [ ] Confirmar conectividade real do ambiente atual para Audit Logs, SAPA e SIGRA.
- [x] Confirmar conectividade real do ambiente atual para LDAP.
- [x] Configurar `NETQ_AUTH_PROVIDER=ldap`.
- [x] Configurar `NETQ_LEGACY_CONFIG_FILE` com o ficheiro legado apropriado ao ambiente real.
- [x] Definir se o teste real vai usar `allowed_users` local ou apenas autenticação LDAP.
- [x] Executar login real no backend novo.
- [x] Validar bootstrap de sessão, keep-alive e logout contra o ambiente real.
- [ ] Implementar contratos funcionais de `Audit Logs` no backend novo para permitir testes reais desse módulo.
- [ ] Implementar fluxo funcional de `SIGRA` no backend/frontend novos para permitir testes reais desse módulo.

### Evidência já validada em ambiente real

- [x] `POST /api/v1/auth/login` autenticou com LDAP real e devolveu `200 OK`.
- [x] `POST /api/v1/auth/login` devolveu `Set-Cookie: netq_session=...`.
- [x] `GET /api/v1/auth/session` devolveu `200 OK` após login real.
- [x] `POST /api/v1/auth/keep-alive` devolveu `200 OK` e renovou a sessão real.
- [x] `DELETE /api/v1/auth/session` devolveu `200 OK` com headers `no-store`.
- [x] `GET /api/v1/auth/session` devolveu `401 Unauthorized` após logout real.

### Sprint 5 — Módulo Navegação principal

- [ ] Migrar shell principal e navegação entre módulos.
- [ ] Reproduzir comportamento do menu principal.
- [x] Implementar estratégia equivalente de keep-alive ou expiração.
- [ ] Homologar paridade funcional da navegação.

### Sprint 6 — Módulo Audit Logs: consulta principal

- [ ] Migrar consulta por ambiente.
  Status:
  em progresso
  Subtasks:
  - [x] Implementar seleção de ambiente no frontend.
  - [x] Mapear ambiente selecionado para `prod` ou `qa` no contrato novo.
  - [ ] Validar chamadas reais aos upstreams corretos por ambiente.
- [ ] Migrar consulta por tipo de ID.
  Status:
  em progresso
  Subtasks:
  - [x] Implementar seleção de tipo de ID no frontend.
  - [x] Mapear tipos `NETQ`, `TIBCO`, `NETWIN`, `SIGRA` e `NA` para a lógica do backend.
  - [ ] Validar o fluxo `NETQ` separadamente do fluxo de ID externo.
- [ ] Migrar consulta por ID.
  Status:
  em progresso
  Subtasks:
  - [x] Implementar campo de entrada e validação básica do ID submetido.
  - [x] Enviar `queryValue` no contrato novo.
  - [x] Exibir resultado, vazio e erro de forma consistente.
- [ ] Definir e validar contrato JSON da consulta principal.
- [ ] Homologar paridade funcional da consulta principal.

### Sprint 7 — Módulo Audit Logs: SAPA e detalhes

- [x] Migrar fluxo de consulta por SAPA ID.
  Subtasks:
  - [x] Implementar envio de `source=sapa-id` e `queryType=SAPA`.
  - [x] Integrar resposta SAPA ao mesmo shell visual de resultados.
  - [x] Validar cenário de sucesso, vazio e erro.
- [ ] Migrar expansão de registos left/right.
  Subtasks:
  - [ ] Implementar carregamento lazy de detalhe relacionado.
  - [ ] Ligar `left` ao payload mongo e `right` ao payload audit.
  - [ ] Validar expansão visual e semântica dos painéis.
- [ ] Migrar pedidos relacionados e detalhes carregados sob demanda.
  Subtasks:
  - [ ] Retornar `relatedOrderIds` estruturados no backend.
  - [ ] Renderizar lista de relacionados no frontend.
  - [ ] Carregar detalhe apenas quando o operador expandir o item.
- [ ] Validar payloads grandes, vazio, timeout e erro externo.
- [ ] Homologar paridade funcional completa do módulo Audit Logs.

### Sprint 8 — Módulo SIGRA

- [ ] Documentar regras de validação de AC.
- [ ] Migrar integração SOAP SIGRA/TIBCO.
  Subtasks:
  - [ ] Implementar endpoint backend para submissão de AC.
  - [ ] Ligar endpoint ao cliente SOAP novo.
  - [ ] Garantir retorno estruturado de request e response.
- [ ] Implementar visualização de request e response.
  Subtasks:
  - [ ] Exibir request XML no frontend.
  - [ ] Exibir response XML no frontend.
  - [ ] Garantir legibilidade de payloads longos no code viewer.
- [ ] Validar cenários de sucesso, erro funcional e timeout.
- [ ] Homologar paridade funcional do módulo SIGRA.

### Sprint 9 — Paridade visual e UX

- [ ] Aplicar design system inspirado na Vercel.
- [ ] Simplificar a tela de login para reduzir ruído visual e excesso de contexto.
  Subtasks:
  - [x] Rever o conteúdo atual do login e remover texto secundário não essencial.
  - [x] Criar 3 propostas visuais de login em imagem para aprovação antes de alterar código.
  - [x] Aprovar uma direção visual final para o login.
  - [x] Refatorar `frontend/app/login/page.tsx` com hierarquia mais limpa e moderna.
  - [x] Ajustar `frontend/app/globals.css` para suportar a nova composição do login.
  - [ ] Validar estados de erro, sessão expirada e responsividade do login simplificado.
- [ ] Refinar layout, hierarquia visual, formulários e estados de loading.
- [ ] Garantir consistência visual entre login, navegação, Audit Logs e SIGRA.
- [ ] Validar que ajustes visuais não alteraram comportamento funcional.

### Sprint 10 — Qualidade e regressão

- [ ] Expandir testes unitários backend e frontend.
- [ ] Consolidar testes de integração com LDAP, HTTP e SOAP.
- [ ] Implementar testes E2E dos fluxos críticos.
- [ ] Executar regressão de paridade funcional ponta a ponta.

### Sprint 11 — Containerização

- [ ] Criar Dockerfile do backend.
- [ ] Criar Dockerfile do frontend.
- [ ] Validar execução local via containers.
- [ ] Externalizar toda a configuração operacional.

### Sprint 12 — Kubernetes

- [ ] Criar manifests ou Helm chart.
- [ ] Configurar Deployment, Service, Ingress, ConfigMap e Secret.
- [ ] Configurar readiness/liveness, requests/limits e rollout.
- [ ] Validar deploy em ambiente de teste no Kubernetes.

### Sprint 13 — Homologação final

- [ ] Executar UAT com checklist baseado no legado.
- [ ] Corrigir gaps de paridade funcional.
- [ ] Validar observabilidade, logs, métricas e operação.
- [ ] Aprovar release candidate.

### Sprint 14 — Cutover e estabilização

- [ ] Executar go-live controlado.
- [ ] Rodar smoke tests pós-deploy.
- [ ] Monitorar erros, latência, integrações e comportamento real.
- [ ] Corrigir desvios rapidamente.
- [ ] Encerrar legado após estabilização aprovada.

## Cronograma sugerido

- [ ] Sprint 0: 2 a 3 dias.
- [ ] Sprint 1 a Sprint 3: 1 semana cada.
- [ ] Sprint 4 a Sprint 10: 1 a 2 semanas cada, conforme complexidade do módulo.
- [ ] Sprint 11 a Sprint 14: 1 semana cada.
- [ ] Revisar duração real ao fim de cada sprint com base no risco e na paridade atingida.

## Notas
- [ ] O frontend deve seguir uma direção visual inspirada na Vercel, sem perder clareza operacional.
- [ ] A prioridade é preservar comportamento funcional antes de otimizações secundárias.
- [ ] O novo sistema não deve depender de Tomcat, WAR, Ant ou configuração em `catalina.base`.
- [ ] Estrutura sugerida do novo projeto: `netq-log-platform/backend`, `netq-log-platform/frontend`, `netq-log-platform/infra`, `netq-log-platform/docs`.
