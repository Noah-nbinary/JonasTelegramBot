from datetime import datetime


class bot_jona():

    def __init__(self, total_ahorros=2374,facturas_mensual=30,
                gasto_mensual=70,ultimo_mes=6,ultimo_año=2027):

        self.total_ahorros = total_ahorros
        self.facturas_mensual = facturas_mensual
        self.gasto_mensual = gasto_mensual
        self.fecha_final = datetime(ultimo_año, ultimo_mes, 1).date()
        self.fecha_actual = datetime.now().date()
        self.meses_restantes = (self.fecha_final.year - self.fecha_actual.year) * 12 \
            + (self.fecha_final.month - self.fecha_actual.month)

        self.attributes = { 
        1:'total_ahorros', 
        2:'facturas_mensual', 
        3:'gasto_mensual'
        }

    def calculate_remaining_months(self):
        calculo_meses_restantes = (self.fecha_final.year - self.fecha_actual.year) * 12 \
            + (self.fecha_final.month - self.fecha_actual.month)
        setattr(self,'meses_restantes',calculo_meses_restantes)
        return
    
    def calculate_surplus(self):
        # El programa interpreta que las facturas y 70€ de este mes ya se han sacado de los ahorros
        return self.total_ahorros - self.meses_restantes * (self.facturas_mensual + self.gasto_mensual)
    
    def calculate_monthly_surplus(self):

        return self.calculate_surplus() / self.meses_restantes + self.gasto_mensual

    def change_value(self, attribute:int,value:int) -> tuple[int,int]:

        print(f'Attr is {attribute} and value is {value}')

        if not attribute or not value:
            raise ValueError

        old_value = getattr(self,self.attributes[attribute])
        setattr(self,self.attributes[attribute],value)
        return getattr(self,self.attributes[attribute]) , old_value

    def display_info(self):

        return f'''
Total Ahorros: {self.total_ahorros} €
Facturas Mensual: {self.facturas_mensual} €
Gasto Mensual: {self.gasto_mensual} €
Surplus Total: {self.calculate_surplus()} €
Media mensual: {self.calculate_monthly_surplus():.2f} €
Meses Restantes: {self.meses_restantes}
Ultimo Mes: {self.fecha_final.strftime("%d/%m/%Y")}

Nota: Se da por hecho que las facturas y gastos del mes en curso, se han restado de los ahorros totales'''
