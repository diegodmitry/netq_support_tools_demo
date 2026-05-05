# Relatório de Segurança

Data da análise: 2026-05-05

Escopo analisado:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform`

Metodologia:
- Revisão estática de código e configuração
- Inspeção de fluxos de autenticação, sessão, integração externa e exposição de segredos
- Não foram executados testes dinâmicos, varredura SAST automatizada nem pentest em execução

## Resumo executivo

O projeto apresenta riscos relevantes em ambos os componentes analisados.

- A aplicação legada `NetQTools` concentra os problemas mais graves: segredos versionados, autenticação LDAP com confiança cega em certificado, endpoints sensíveis potencialmente acessíveis sem validação de sessão e saída HTML montada com dados não escapados.
- A plataforma nova `netq-log-platform` melhora a organização do código, mas ainda tem uma falha crítica de autorização: os endpoints backend de consulta de auditoria não validam autenticação no servidor e podem ser acessados diretamente se o serviço estiver exposto na rede.
- Também há fragilidades operacionais importantes, como uso de HTTP sem TLS para integrações internas e mecanismos de bypass/mock de autenticação que precisam de controles rígidos de deploy.

## Achados prioritários

### 1. Crítico: segredos reais e credenciais internas armazenados no repositório

Impacto:
- Comprometimento imediato de credenciais de usuário, credenciais técnicas LDAP e autenticação básica de integrações
- Movimento lateral para serviços internos
- Risco de vazamento duradouro mesmo após remoção do arquivo, se o histórico Git já foi compartilhado

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/login.example.json:4`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_PRD.json:6`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_PRD.json:24`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_DEV.json:6`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_DEV.json:24`

Detalhe:
- O repositorio continha um `login.json` com `username` e `password`; ele foi convertido para `login.example.json`.
- Os arquivos legados `app_PRD.json`, `app_DEV.json` e `app.json` continham senha de basic auth e senha do bind LDAP; os valores do working tree atual foram substituidos por placeholders.

Recomendação:
- Rotacionar imediatamente todas as credenciais expostas.
- Remover segredos do repositório e do histórico.
- Adotar somente secret manager ou arquivos montados fora do versionamento.
- Adicionar varredura de segredos no pipeline.

### 2. Crítico: endpoints backend de auditoria sem autenticação/autorização no servidor

Impacto:
- Qualquer cliente que alcance o backend pode consultar logs e payloads sensíveis sem sessão válida
- A proteção atual fica dependente apenas do frontend/proxy, o que não é controle de segurança suficiente

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend/app/api/routes/audit_logs.py:18`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend/app/api/routes/audit_logs.py:34`
- Em contraste, a sessão só é validada nos fluxos de auth em `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend/app/application/auth/service.py:93`
- O frontend apenas repassa o cookie em `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/frontend/shared/lib/auth-client.server.ts:130`

Detalhe:
- As rotas `/audit-logs/query` e `/audit-logs/related-detail` não usam dependência de autenticação nem verificam sessão.
- Se o backend FastAPI estiver exposto por ingress, service mesh ou porta local acessível, o atacante pode chamar a API diretamente.

Recomendação:
- Exigir autenticação e autorização no backend para todas as rotas de negócio.
- Implementar uma dependência obrigatória que valide a sessão antes de executar `AuditLogsService`.
- Restringir exposição de rede do backend enquanto a correção não é aplicada.

### 3. Alto: aplicação legada aceita LDAP sobre TLS sem validar certificado

Impacto:
- Permite ataque man-in-the-middle na autenticação LDAP
- Credenciais de usuários e credenciais técnicas podem ser interceptadas

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/Login.java:68`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/Login.java:72`
- O componente novo também admite desabilitar validação em `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/k8s/base/backend-configmap.yaml:17`

Detalhe:
- O legado usa `TrustAllTrustManager`, que invalida o objetivo do LDAPS.
- No deployment novo, `NETQ_LDAP_VALIDATE_CERTIFICATES` está definido como `"false"`.

Recomendação:
- Remover `TrustAllTrustManager`.
- Instalar cadeia de CA confiável no runtime.
- Bloquear promoção para produção quando a validação de certificado estiver desativada.

### 4. Alto: servlets legados de consulta parecem acessíveis sem validação explícita de sessão

Impacto:
- Possível acesso direto a consultas operacionais e integrações sensíveis sem login
- Bypass de proteção de tela/JSP por chamada direta ao servlet

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequest.java:44`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequest.java:179`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequestSigra.java:42`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequestSigra.java:116`

Detalhe:
- Os servlets processam requisições GET e POST, consomem parâmetros do usuário e executam lógica de integração.
- Não há checagem local de `LOGGED_USERNAME` ou filtro de autenticação nesses endpoints.
- A proteção observada está na JSP `menu.jsp`, o que não impede acesso direto ao servlet.

Recomendação:
- Adicionar validação de sessão em todos os servlets sensíveis.
- Preferir filtro servlet centralizado para autenticação/autorização.
- Restringir métodos e rotas até a correção.

### 5. Alto: saída HTML legada é construída com dados não escapados, com risco de XSS

Impacto:
- Execução de JavaScript no navegador do operador
- Roubo de sessão, falsificação de ações e exfiltração de dados visualizados

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequest.java:96`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequest.java:99`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequest.java:109`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequest.java:157`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/URLRequestSigra.java:93`

Detalhe:
- Parâmetros e payloads externos são concatenados diretamente em HTML.
- Como o sistema exibe respostas de integrações e XMLs externos, o vetor não depende apenas de input local do usuário.

Recomendação:
- Escapar toda saída HTML.
- Renderizar payloads apenas como texto.
- Aplicar CSP e remover concatenação manual em servlets/JSPs.

### 6. Alto: integrações internas usam HTTP sem TLS

Impacto:
- Interceptação e alteração de tráfego interno
- Exposição de dados operacionais e credenciais basic auth em rede

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_PRD.json:3`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_PRD.json:7`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/conf/app_PRD.json:15`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/k8s/base/backend-configmap.yaml:18`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/k8s/base/backend-configmap.yaml:21`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/k8s/base/backend-configmap.yaml:28`

Recomendação:
- Migrar integrações para HTTPS ou túnel autenticado.
- Impedir envio de basic auth por HTTP puro.

## Achados secundários

### 7. Médio: modo de autenticação mock e bypass habilitáveis por configuração

Impacto:
- Se variáveis de ambiente incorretas forem promovidas, a aplicação pode autenticar usuários sem LDAP real

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend/app/core/config.py:28`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/backend/app/core/config.py:45`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/frontend/shared/lib/dev-auth.ts:1`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/netq-log-platform/frontend/proxy.ts:6`

Detalhe:
- O backend sobe por padrão com `auth_provider = "mock"` e `mock_password = "secret"`.
- O frontend admite bypass com `NETQ_SKIP_AUTH=true`.

Recomendação:
- Falhar o startup fora de ambiente local quando mock/bypass estiver habilitado.
- Separar builds de desenvolvimento e produção.

### 8. Médio: cookies/sessão no legado sem flags de segurança explícitas

Impacto:
- Maior exposição a roubo de cookie e abuso em cenários com XSS ou tráfego inseguro

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/Login.java:97`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/src/java/NetqTools/SessionPing.java:34`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/web/WEB-INF/web.xml:14`

Detalhe:
- Não foram encontrados ajustes explícitos de `HttpOnly`, `Secure` e `SameSite` no legado.
- O código manipula cookies de sessão diretamente, o que aumenta a chance de configuração inconsistente.

Recomendação:
- Configurar flags de cookie no container e na aplicação.
- Renovar sessão após login.

### 9. Médio: bibliotecas legadas antigas aumentam superfície de vulnerabilidade conhecida

Evidências:
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/web/js/jquery-1.12.4.js:2`
- `/Users/diegodmitry/Documents/Projects.nosync/netq_support_tools/NetQTools/web/js/highlight.pack.js:1`

Detalhe:
- `jQuery 1.12.4` e `highlight.js 9.12.0` estão muito defasados.

Recomendação:
- Atualizar dependências do legado ou isolar a aplicação até descontinuação.

## Pontos positivos

- O backend novo usa tipagem e validação com Pydantic nas rotas.
- Os cookies da plataforma nova são emitidos com `HttpOnly` e `SameSite=Lax`.
- Há preocupação explícita com secrets montados por arquivo no backend novo.

## Plano de remediação recomendado

### Imediato

1. Rotacionar todas as credenciais expostas e invalidar qualquer senha ou usuário técnico comprometido.
2. Manter `login.example.json` e os arquivos legados apenas com placeholders, sem restaurar segredos reais no repositório.
3. Proteger no backend as rotas `/audit-logs/*` com validação obrigatória de sessão.
4. Bloquear deploy com `NETQ_SKIP_AUTH=true`, `auth_provider=mock` ou `NETQ_LDAP_VALIDATE_CERTIFICATES=false`.

### Curto prazo

1. Corrigir o legado para validar sessão em todos os servlets.
2. Eliminar `TrustAllTrustManager` e restaurar validação de certificado LDAP.
3. Escapar toda saída HTML do legado e reduzir renderização direta de payload.
4. Migrar integrações internas críticas para transporte cifrado.

### Médio prazo

1. Introduzir SAST, secret scanning e policy checks no CI.
2. Revisar modelo de autorização por perfil e trilha de auditoria.
3. Planejar retirada controlada da aplicação legada `NetQTools`.

## Conclusão

O risco atual do repositório é alto. O ponto mais urgente é a combinação de segredos expostos com controles insuficientes de autenticação/autorização, especialmente no backend novo e na aplicação legada. Antes de qualquer exposição ampliada do sistema, vale tratar pelo menos os itens críticos e altos deste relatório.
