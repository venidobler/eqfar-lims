import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from equipments.models import Equipment
from laboratory.models import Consumable, Analysis, EquipmentBooking, MaterialUsage

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para o LIMS'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Iniciando o processo de semeadura...')

        # 1. Criar Usuários de Teste
        researchers = []
        names = ['Ana Silva', 'Carlos Souza', 'Beatriz Lima', 'Dr. House']
        for name in names:
            username = name.lower().replace(' ', '').replace('.', '')
            user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@lab.com'})
            if created:
                user.set_password('123')
                user.save()
            researchers.append(user)
        
        # Adicionar o seu superuser atual na lista para ter dados seus também
        superusers = User.objects.filter(is_superuser=True)
        if superusers.exists():
            researchers.extend(list(superusers))

        self.stdout.write(f'✅ {len(researchers)} pesquisadores prontos.')

        # 2. Criar Equipamentos
        eq_names = [
            ('HPLC Agilent 1260', 'Agilent', 'Cromatografia'),
            ('Espectrofotômetro UV-Vis', 'Shimadzu', 'Espectroscopia'),
            ('Balança Analítica', 'Mettler Toledo', 'Pesagem'),
            ('Dissolutor 708-DS', 'Agilent', 'Dissolução'),
            ('GC-MS Cromatógrafo Gás', 'Thermo Fisher', 'Cromatografia'),
        ]
        equipments = []
        for name, brand, model in eq_names:
            eq, _ = Equipment.objects.get_or_create(
                name=name, 
                defaults={'brand': brand, 'model': model, 'asset_tag': f'TAG-{random.randint(1000,9999)}'}
            )
            equipments.append(eq)
        self.stdout.write(f'✅ {len(equipments)} equipamentos prontos.')

        # 3. Criar Insumos (Consumables)
        cons_data = [
            ('Metanol HPLC Grade', 'L', 45.00),
            ('Acetonitrila', 'L', 120.50),
            ('Água Mili-Q', 'L', 5.00),
            ('Filtro Seringa 0.45um', 'un', 2.50),
            ('Vial de Vidro Ambar', 'un', 1.20),
            ('Coluna C18 150mm', 'un', 2500.00),
        ]
        consumables = []
        for name, unit, cost in cons_data:
            cons, _ = Consumable.objects.get_or_create(
                name=name,
                defaults={'unit': unit, 'cost_per_unit': cost, 'current_stock': random.randint(50, 500)}
            )
            consumables.append(cons)
        self.stdout.write(f'✅ {len(consumables)} insumos prontos.')

        # 4. Criar Análises e Agendamentos
        self.stdout.write('🧪 Gerando análises e agendamentos (isso pode levar uns segundos)...')
        
        titles = [
            'Controle de Qualidade - Lote {}',
            'Estabilidade Acelerada - {}',
            'Desenvolvimento Metodológico - {}',
            'Análise de Impurezas - {}'
        ]

        # Gera dados para hoje e os próximos 5 dias
        base_time = timezone.now().replace(minute=0, second=0, microsecond=0)
        
        for i in range(15): # Criar 15 análises
            researcher = random.choice(researchers)
            title = random.choice(titles).format(random.randint(100, 999))
            
            analysis = Analysis.objects.create(
                title=title,
                description="Análise gerada automaticamente pelo sistema de seeds.",
                project_name="Projeto Genérico 2026",
                researcher=researcher,
                status=random.choice(['planned', 'ongoing', 'approved'])
            )

            # Adicionar Consumo de Material
            for _ in range(random.randint(1, 3)):
                MaterialUsage.objects.create(
                    analysis=analysis,
                    consumable=random.choice(consumables),
                    quantity_used=random.uniform(1.0, 50.0)
                )

            # Tentar criar um agendamento sem conflito
            # Vamos tentar 3 slots aleatórios, se der certo, salva
            equipment = random.choice(equipments)
            
            # Escolhe um dia aleatório entre hoje e +5 dias
            day_offset = random.randint(0, 5)
            # Escolhe uma hora entre 08:00 e 16:00
            hour_offset = random.randint(8, 16)
            
            start_time = base_time + timedelta(days=day_offset, hours=hour_offset)
            end_time = start_time + timedelta(hours=random.randint(1, 4)) # Duração de 1 a 4 horas

            # Verifica conflito "na mão" para não quebrar o script
            conflict = EquipmentBooking.objects.filter(
                equipment=equipment,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if not conflict:
                EquipmentBooking.objects.create(
                    analysis=analysis,
                    equipment=equipment,
                    start_time=start_time,
                    end_time=end_time
                )

        self.stdout.write(self.style.SUCCESS('🎉 Dados de teste criados com sucesso!'))