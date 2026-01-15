from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from equipments.models import Equipment  # Importando do outro app

# --- 1. Tabela de Insumos (Consumables) ---
class Consumable(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Insumo")
    unit = models.CharField(max_length=20, verbose_name="Unidade (ex: mL, g, un)")
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Estoque Atual")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Custo Unitário (R$)")

    def __str__(self):
        return f"{self.name} ({self.unit})"

# --- 2. Tabela Pai: A Análise (Analysis) ---
class Analysis(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planejada'),
        ('ongoing', 'Em Andamento'),
        ('approved', 'Aprovada / Concluída'),
        ('rejected', 'Rejeitada / Cancelada'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título da Análise")
    description = models.TextField(blank=True, verbose_name="Descrição / Metodologia")
    project_name = models.CharField(max_length=150, blank=True, verbose_name="Projeto de Pesquisa")
    
    researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analyses', verbose_name="Pesquisador Responsável")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.researcher.username}"

# --- 3. Tabela de Agendamento (EquipmentBooking) ---
# Substitui a antiga tabela 'Scheduling'
class EquipmentBooking(models.Model):
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='bookings')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='bookings')
    
    start_time = models.DateTimeField(verbose_name="Início")
    end_time = models.DateTimeField(verbose_name="Fim")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']
        verbose_name = "Reserva de Equipamento"
        verbose_name_plural = "Reservas de Equipamentos"

    def __str__(self):
        return f"{self.equipment.name} | {self.start_time.strftime('%d/%m %H:%M')}"

    # Regra de Negócio: Anti-Conflito (Mantivemos a lógica!)
    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("O horário final deve ser posterior ao inicial.")
            
            # Busca conflitos
            conflicts = EquipmentBooking.objects.filter(
                equipment=self.equipment,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            
            # Se for edição, exclui o próprio ID da verificação
            if self.pk:
                conflicts = conflicts.exclude(pk=self.pk)
            
            if conflicts.exists():
                raise ValidationError(f"O equipamento '{self.equipment.name}' já está ocupado neste horário.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# --- 4. Tabela Pivô: Uso de Material (MaterialUsage) ---
class MaterialUsage(models.Model):
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='materials_used')
    consumable = models.ForeignKey(Consumable, on_delete=models.PROTECT) # Protect: não deixa apagar insumo se já foi usado
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade Usada")

    def total_cost(self):
        return self.quantity_used * self.consumable.cost_per_unit

    def __str__(self):
        return f"{self.consumable.name}: {self.quantity_used}"