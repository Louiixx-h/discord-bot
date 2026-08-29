# Bot Discord para amigos

Bot completo para Discord escrito em Python 3.11+ com `discord.py`. Ele recebe e
despede membros, recomenda jogos com `/jogo`, conta piadas com `/joke`, mede a
aura com `/aura`, aplica uma zika com `/zika`, mostra as regras com `/regras` e
publica uma piada diária em um horário e timezone configuráveis.

## Funcionalidades

- mensagem de boas-vindas com menção restrita ao membro que entrou;
- mensagem de saída tolerante a canal removido e falta de permissão;
- `/jogo` com catálogo editável, embed e cooldown individual de três segundos;
- `/joke` para contar uma das piadas cadastradas sem repetição consecutiva;
- `/aura` para sortear entre `-10000` e `+1100` de aura para outro membro;
- `/zika` para anunciar, com menção controlada, que um membro foi zikado;
- `/regras` com as dez regras centralizadas em um módulo de dados;
- piada diária com 35 opções, timezone IANA e tarefa assíncrona;
- persistência atômica do último envio para não repetir a piada anterior nem
  publicar duas vezes no mesmo dia após um reinício;
- sincronização rápida em um servidor de desenvolvimento ou sincronização global;
- validação de configuração, logs sem credenciais e tratamento global de erros.

## Estrutura

```text
.
├── bot/
│   ├── cogs/
│   │   ├── games.py
│   │   ├── jokes.py
│   │   ├── rules.py
│   │   ├── social.py
│   │   └── welcome.py
│   ├── data/
│   │   ├── games.py
│   │   ├── jokes.py
│   │   └── rules.py
│   ├── utils/
│   │   ├── channels.py
│   │   └── joke_state.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── client.py
│   ├── config.py
│   └── main.py
├── tests/
│   ├── test_config.py
│   ├── test_data.py
│   ├── test_jokes.py
│   └── test_social.py
├── .env.example
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Pré-requisitos

- Python 3.11 ou superior;
- uma conta Discord com permissão para administrar um servidor de testes;
- Git, recomendado para controle de versão.

Confira a versão instalada:

```bash
python --version
```

Em algumas distribuições Linux/macOS, o comando é `python3` em vez de `python`.

## 1. Criar a aplicação e o bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Selecione **New Application**, informe um nome e crie a aplicação.
3. Abra a seção **Bot** e selecione **Add Bot**, caso ela ainda não exista.
4. Nessa mesma seção, use **Reset Token** quando precisar gerar um token e copie-o
   diretamente para o seu arquivo `.env` local.

O token autentica o bot e deve ser tratado como uma senha. Não o envie em chats,
prints, commits, tickets ou logs. Se ele vazar, redefina-o imediatamente no portal.

## 2. Configurar Gateway Intents

Na página **Bot**, em **Privileged Gateway Intents**, ative apenas:

- **Server Members Intent**: necessário para os eventos de entrada e saída.

O código ativa somente `guilds` e `members`. **Message Content Intent** e
**Presence Intent** não são necessários e devem permanecer desativados.

## 3. Configurar OAuth2 e convidar o bot

1. No Developer Portal, abra **OAuth2 > URL Generator** (ou a página equivalente
   de instalação da aplicação).
2. Selecione os escopos `bot` e `applications.commands`.
3. Marque somente estas permissões do bot:
   - **View Channels**;
   - **Send Messages**;
   - **Embed Links**.
4. Abra a URL gerada, escolha o servidor e confirme a autorização.

Não conceda **Administrator**. Caso o servidor use permissões específicas por
canal, permita ao bot visualizar e enviar mensagens nos dois canais configurados.

## 4. Criar e ativar o ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Prompt de Comando:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

## 5. Instalar as dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

As únicas dependências diretas são `discord.py`, `python-dotenv` e `tzdata`. A
última fornece a base de timezones em sistemas, como algumas instalações do
Windows, que não a incluem nativamente.

## 6. Configurar o `.env`

Copie o exemplo sem sobrescrever um `.env` existente:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edite o `.env`:

```dotenv
DISCORD_TOKEN=
GUILD_ID=
WELCOME_CHANNEL_ID=
GENERAL_CHANNEL_ID=
DEV_GUILD_ID=
TIMEZONE=America/Sao_Paulo
DAILY_JOKE_TIME=12:00
JOKE_STATE_FILE=.state/joke_state.json
LOG_LEVEL=INFO
```

Variáveis:

| Variável | Obrigatória | Descrição |
|---|---:|---|
| `DISCORD_TOKEN` | sim | Token secreto obtido no Developer Portal. |
| `WELCOME_CHANNEL_ID` | sim | Canal das mensagens de entrada e saída. |
| `GENERAL_CHANNEL_ID` | sim | Canal que recebe a piada diária. |
| `GUILD_ID` | não | Se definido, limita eventos e a piada a esse servidor. |
| `DEV_GUILD_ID` | não | Sincroniza comandos apenas nesse servidor para testes rápidos. |
| `TIMEZONE` | não | Nome IANA; padrão `America/Sao_Paulo`. |
| `DAILY_JOKE_TIME` | não | Horário local em `HH:MM`; padrão `12:00`. |
| `JOKE_STATE_FILE` | não | Estado local; padrão `.state/joke_state.json`. |
| `LOG_LEVEL` | não | `CRITICAL`, `ERROR`, `WARNING`, `INFO` ou `DEBUG`. |

Para copiar IDs, ative **Configurações do usuário > Avançado > Modo de
desenvolvedor** no Discord, clique com o botão direito no servidor/canal e use
**Copiar ID**. IDs vazios opcionais são aceitos; os obrigatórios devem conter
somente dígitos e estar dentro do intervalo de um Snowflake do Discord.

Nunca coloque comentários na mesma linha do token. O `.gitignore` exclui `.env`,
mas confirme com `git status` antes de cada commit.

## 7. Executar

Com o ambiente virtual ativo e o `.env` preenchido:

```bash
python -m bot
```

Também é possível executar:

```bash
python -m bot.main
```

O processo valida toda a configuração antes de se conectar. Erros informam apenas
o nome da variável problemática e nunca exibem o token ou seu valor.

## 8. Testar os Slash Commands

Durante o desenvolvimento, preencha `DEV_GUILD_ID` com o ID do servidor de testes
e reinicie o bot. Os comandos `/jogo`, `/joke`, `/aura`, `/zika` e `/regras` são
sincronizados somente nesse servidor e costumam aparecer rapidamente.

Para produção, deixe `DEV_GUILD_ID=` vazio e reinicie. A sincronização será global;
a propagação global é controlada pelo Discord e pode demorar. A sincronização roda
uma vez no `setup_hook` por processo, não em cada reconexão do WebSocket.

No Discord:

1. digite `/jogo` e confirme o embed com nome, descrição, jogadores, tipo e
   plataformas;
2. tente usá-lo novamente imediatamente e confirme a mensagem de cooldown;
3. digite `/joke` e confira uma piada do catálogo;
4. use `/aura membro:@alguém` e confirme o valor entre `-10000` e `+1100`;
5. use `/zika membro:@alguém` e confira a menção controlada;
6. digite `/regras` e confira as dez regras;
7. use contas de teste para validar as mensagens de entrada e saída;
8. temporariamente configure `DAILY_JOKE_TIME` para alguns minutos à frente para
   validar a tarefa diária.

Execute também os testes locais:

```bash
python -m unittest discover -s tests -v
```

## 9. Alterar o conteúdo

- Jogos: edite `bot/data/games.py` e acrescente outro `Game(...)` à tupla `GAMES`.
- Piadas: edite `bot/data/jokes.py` e acrescente uma string à tupla `JOKES`.
- Regras: edite a ordem ou o texto da tupla `RULES` em `bot/data/rules.py`.

Não é preciso alterar as Cogs para adicionar conteúdo. Mantenha textos dentro dos
limites de mensagens e embeds do Discord.

## 10. Configurar a piada diária

`DAILY_JOKE_TIME` representa o horário no timezone definido por `TIMEZONE`. Por
exemplo:

```dotenv
TIMEZONE=America/Sao_Paulo
DAILY_JOKE_TIME=18:30
```

A tarefa usa um horário com timezone via `discord.ext.tasks`. O arquivo definido
em `JOKE_STATE_FILE` guarda somente o índice da última piada e a data do último
envio. Ele é atualizado atomicamente, não contém mensagens de usuários e fica fora
do Git. Se o canal não existir, não for textual ou não permitir envio, a falha é
registrada e a tarefa tentará novamente no próximo horário sem encerrar o bot.

## Segurança adotada

- segredos apenas no ambiente/`.env`, excluído do Git;
- `Settings.token` não aparece nem em sua representação de depuração;
- validação antecipada dos IDs, horário, timezone, nível de log e campos obrigatórios;
- menor privilégio: dois intents e três permissões de canal, sem Administrator;
- `AllowedMentions` bloqueia `@everyone`, `@here` e cargos; boas-vindas permitem
  somente a menção do membro conhecido pelo evento;
- nenhum `eval`, `exec`, shell, download, URL ou acesso a arquivo controlado por
  usuários do Discord;
- cooldown por usuário em `/jogo`, `/joke`, `/aura` e `/zika`, além do respeito
  ao rate limit nativo da biblioteca;
- tratamento de canal ausente, tipo incorreto, falta de permissão e erros HTTP;
- mensagens de erro para usuários são genéricas; logs não incluem conteúdo privado;
- dependências diretas conhecidas e fixadas no `requirements.txt`.

## Deploy no Northflank com Docker

O projeto inclui um `Dockerfile` baseado na imagem oficial
`python:3.12.14-slim-bookworm`. A imagem instala apenas as dependências de
produção, não inclui o `.env` e executa o bot como um usuário sem privilégios.

Antes do deploy, envie o projeto para um repositório Git que o Northflank possa
acessar. Depois:

1. crie um projeto no Northflank;
2. crie um **Combined Service**;
3. selecione o repositório e a branch do bot;
4. escolha **Dockerfile** como método de build;
5. informe `/Dockerfile` como caminho e `/` como contexto de build;
6. não configure porta pública nem health check HTTP;
7. mantenha exatamente **1 instance/replica** e desative autoscaling;
8. cadastre as variáveis abaixo em **Runtime environment**;
9. faça o deploy e confira nos logs se as Cogs e os comandos foram sincronizados.

Variáveis mínimas de runtime:

```dotenv
DISCORD_TOKEN=seu_token_no_painel_do_northflank
WELCOME_CHANNEL_ID=id_do_canal
GENERAL_CHANNEL_ID=id_do_canal
TIMEZONE=America/Sao_Paulo
DAILY_JOKE_TIME=12:00
JOKE_STATE_FILE=/app/.state/joke_state.json
LOG_LEVEL=INFO
```

Também configure `DEV_GUILD_ID` para sincronização imediata em um servidor de
testes e, opcionalmente, `GUILD_ID` para restringir o bot a um servidor. Salve o
token diretamente nas variáveis protegidas do Northflank: nunca envie o `.env`
para o Git ou use o token como build argument.

O diretório `/app/.state` é gravável, mas o armazenamento padrão do container é
efêmero. Para preservar a data e o índice da última piada entre novos deployments,
monte um volume persistente em `/app/.state`. Sem volume, o bot continua
funcionando, mas pode perder esse pequeno histórico quando o container for recriado.

Teste a imagem localmente, sem gravar o token nela:

```bash
docker build --tag discord-friends-bot .
docker run --rm --env-file .env discord-friends-bot
```

## Manutenção e hospedagem futura

Para uma máquina local, execute o bot após cada reinicialização usando um gerenciador
de processos apropriado. Em produção, prefira um serviço que reinicie o processo em
falhas e injete as variáveis de ambiente sem gravá-las na imagem ou no repositório:

- Linux: unidade `systemd` executando `.venv/bin/python -m bot` com usuário sem
  privilégios;
- contêiner: imagem Python não-root e segredo fornecido pela plataforma em runtime;
- PaaS/VPS: processo worker persistente, armazenamento gravável para `.state/` e
  logs coletados pela plataforma.

Use Python 3.11+, instale sempre a partir de `requirements.txt`, preserve o arquivo
de estado entre reinícios e configure alertas para encerramentos repetidos. Antes de
atualizar dependências, leia as notas de versão, rode os testes e valide os comandos
no `DEV_GUILD_ID`.
#   d i s c o r d - b o t  
 
