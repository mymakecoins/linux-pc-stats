# linux-stats — Utilitário para a barra do sistema

Aplicação modular em Python que exibe telemetria do sistema e previsão do tempo na **barra do sistema** (barra do Gerenciador de Tarefas, próximo ao relógio e ícones) em Linux.

## Onde está o código

Todo o código da aplicação, scripts de instalação e configuração estão na pasta **project/**:

- **Executar / instalar a partir da pasta project:**  
  `cd project && ./install.sh` e depois `./run-statusbar.sh`
- **Documentação da aplicação:** [project/README.md](project/README.md)

## Conteúdo na raiz

- **docs/**: requisitos, análise técnica, plano de desenvolvimento, integração com a barra do sistema, empacotamento .deb.
- **debian/**: arquivos para gerar o pacote .deb (instala em `/usr/share/linux-stats/` e no executável `/usr/bin/linux-stats-statusbar` — o nome em inglês "status bar" equivale a "barra do sistema").
- **project/**: aplicação completa (src, config, install.sh, run-statusbar.sh, scripts).

## Gerar o pacote .deb

Na raiz do repositório:

```bash
dpkg-buildpackage -us -uc -b
sudo dpkg -i ../linux-stats_*.deb
```

Documentação detalhada: [docs/EMPACOTAMENTO_DEB.md](docs/EMPACOTAMENTO_DEB.md).
