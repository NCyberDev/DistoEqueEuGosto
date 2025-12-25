# Disto é que eu gosto! - Landing Page

Landing page dedicada ao segmento de rádio "Disto é que eu gosto!" apresentado por Jaime Coelho na RCM - Rádio do Concelho de Mafra.

## 🔗 Link (GitHub Pages)

`http://ncyberdev.github.io/DistoEqueEuGosto`

## 📱 QR Code (abre a página)

[![QR code para http://ncyberdev.github.io/DistoEqueEuGosto](https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=http%3A%2F%2Fncyberdev.github.io%2FDistoEqueEuGosto)](http://ncyberdev.github.io/DistoEqueEuGosto)

## 🚀 Deploy para GitHub Pages

### Passo 1: Criar repositório no GitHub

1. Vai a [github.com](https://github.com) e faz login
2. Clica em "New repository" (botão verde)
3. Nome do repositório: `DistoEqueEuGosto` (ou outro nome à tua escolha)
4. **NÃO** inicializes com README, .gitignore ou licença (já temos)
5. Clica em "Create repository"

### Passo 2: Fazer push do código

No terminal, executa:

```bash
git remote add origin https://github.com/SEU_USERNAME/DistoEqueEuGosto.git
git push -u origin main
```

(Substitui `SEU_USERNAME` pelo teu username do GitHub)

### Passo 3: Ativar GitHub Pages

1. No repositório do GitHub, vai a **Settings** (no topo)
2. No menu lateral, clica em **Pages**
3. Em **Source**, escolhe **Deploy from a branch**
4. Escolhe a branch **main** e a pasta **/ (root)**
5. Clica em **Save**

A tua página estará disponível em:
`https://SEU_USERNAME.github.io/DistoEqueEuGosto/`

(Aguarda 1-2 minutos para o primeiro deploy)

## 📱 Gerar QR Code

Depois de teres o URL da página, podes gerar um QR code em:

- [QR Code Generator](https://www.qr-code-generator.com/)
- [QRCode Monkey](https://www.qrcode-monkey.com/)

Basta colar o URL da tua página e gerar o código.

## ➕ Adicionar Novas Gravações

1. Grava o segmento usando `record_radio.py`
2. Move o ficheiro MP3 para a pasta `recordings/`
3. Abre `index.html` e adiciona um novo bloco na secção de gravações:

```html
<article class="episode">
    <h3>21 de Dezembro, 2025 - 10:00</h3>
    <audio controls preload="metadata">
        <source src="recordings/radio_mafra_20251221_100000.mp3" type="audio/mpeg">
        O seu navegador não suporta o elemento de áudio.
    </audio>
</article>
```

4. Faz commit e push:

```bash
git add index.html recordings/
git commit -m "Adicionar nova gravação"
git push
```

## 📝 Notas

- A página é totalmente responsiva e otimizada para mobile
- Os ficheiros de áudio são servidos diretamente do GitHub
- Para ficheiros grandes (>100MB), considera usar GitHub LFS ou um serviço externo
