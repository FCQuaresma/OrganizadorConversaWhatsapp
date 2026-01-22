# 📄 Monta Conversa / Pasta em PDF A4 (com anexos)

Script em Python que **gera um PDF em formato A4**, reunindo automaticamente o conteúdo de uma pasta (inclusive subpastas), na ordem dos arquivos por data de modificação.

✅ Suporta:
- **Textos:** `.txt` e `.md` (com quebra automática de linha + paginação sem cortar)
- **Imagens:** `.jpg`, `.jpeg`, `.png` (centralizadas e redimensionadas para caber no A4 sem cortes)
- **Outros arquivos:** adicionados como **ANEXOS do PDF** (ex: `.mp3`, `.docx`, `.pdf`, `.zip`, etc)

---

## 🚀 O que o script faz?

Ao executar, o script:

1. Varre todos os arquivos da pasta informada (incluindo subpastas)
2. Ordena os arquivos por **data de modificação**
3. Gera um PDF temporário com:
   - imagens em páginas A4 completas (sem cortar)
   - textos com quebra automática e paginação (sem cortar)
4. Adiciona ao PDF final os **arquivos não suportados** como **anexos**
5. Salva o resultado como um PDF final pronto para enviar/arquivar

