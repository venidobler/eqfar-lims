from django.db import models
from django.conf import settings
from equipments.models import Equipment

class Scheduling(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PEND', 'Pendente/Agendado'
        CONFIRMADO = 'CONF', 'Confirmado'
        EM_ANDAMENTO = 'EXEC', 'Em Execução'
        CONCLUIDO = 'CONC', 'Concluído'
        CANCELADO = 'CANC', 'Cancelado'

    equipment = models.ForeignKey(
        Equipment, 
        on_delete=models.CASCADE,
        related_name='schedulings',
        verbose_name="Equipamento"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedulings',
        verbose_name="Solicitante"
    )

    # Essencial para o Gráfico de Gantt
    start_time = models.DateTimeField(verbose_name="Início Previsto")
    end_time = models.DateTimeField(verbose_name="Fim Previsto")
    
    # Para calcular custo real depois
    real_start_time = models.DateTimeField(null=True, blank=True, verbose_name="Início Real")
    real_end_time = models.DateTimeField(null=True, blank=True, verbose_name="Fim Real")

    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.PENDENTE,
        verbose_name="Status"
    )
    
    purpose = models.CharField(max_length=200, verbose_name="Finalidade/Projeto")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.equipment.name} - {self.start_time.strftime('%d/%m %H:%M')}"

    @property
    def duration_hours(self):
        """Calcula a duração prevista em horas"""
        diff = self.end_time - self.start_time
        return diff.total_seconds() / 3600
    
    @property
    def estimated_cost(self):
        """Calcula o custo baseado na hora do equipamento"""
        return self.duration_hours * float(self.equipment.cost_per_hour)