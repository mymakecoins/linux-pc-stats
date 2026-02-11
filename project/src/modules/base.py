"""
Contrato base para módulos de telemetria/dados.
Cada módulo deve retornar um fragmento de linha para a barra do sistema ou N/A em falha.
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseModule(ABC):
    """Interface dos módulos exibidos na barra do sistema."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Identificador do módulo (ex.: 'cpu')."""
        ...

    @property
    def fallback_label(self) -> str:
        """Rótulo usado em fallback (ex.: 'CPU: N/A'). Padrão: name em maiúsculas."""
        return self.name.upper()

    @abstractmethod
    def get_output(self, config: dict[str, Any] | None = None) -> str:
        """
        Retorna o texto a ser exibido na barra para este módulo.
        Em caso de falha, retorna uma string que inclui 'N/A' para manter consistência.
        config: configuração global (opcional, para parâmetros por módulo).
        """
        ...
