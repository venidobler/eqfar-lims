from django.db import models

class Equipment(models.Model):
    class Status(models.TextChoices):
        DISPONIVEL = 'DISP', 'Disponível'
        EMPRESTADO = 'OCUP', 'Ocupado/Em Uso' # Mudei de EMPRESTADO para OCUPADO
        MANUTENCAO = 'MAN', 'Em Manutenção'
        QUEBRADO = 'QUE', 'Quebrado/Inutilizável'

    name = models.CharField(max_length=100, verbose_name="Nome do Equipamento")
    asset_tag = models.CharField(max_length=50, unique=True, verbose_name="Patrimônio/Tag")
    brand = models.CharField(max_length=100, verbose_name="Marca", blank=True, null=True)
    model = models.CharField(max_length=100, verbose_name="Modelo", blank=True, null=True)
    
    # --- NOVOS CAMPOS PARA GESTÃO DE CAPACIDADE ---
    analysis_time_minutes = models.PositiveIntegerField(
        default=60, 
        verbose_name="Tempo Médio por Análise (min)",
        help_text="Tempo estimado para uma análise completa neste equipamento."
    )
    
    cost_per_hour = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="Custo por Hora (R$)"
    )
    # ----------------------------------------------

    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.DISPONIVEL,
        verbose_name="Status Atual"
    )

    photo = models.ImageField(upload_to='equipments/', verbose_name="Foto", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Cadastrado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.asset_tag})"