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

        self.attributes = { 1:'self.total_ahorros', 2:'self.facturas_mensual', 
                    3:'self.gasto_mensual'}
    
    def calculate_surplus(self):
        # El programa interpreta que las facturas y 70€ de este mes ya se han sacado de los ahorros
        return self.total_ahorros - self.meses_restantes * (self.facturas_mensual + self.gasto_mensual)
    
    def calculate_monthly_surplus(self):

        return self.calculate_surplus() / self.meses_restantes + self.gasto_mensual

    def change_value(self, attribute:int=None,value:int=None) -> tuple[int,int]:

        # If attributes are passed, non-verbose
        if attribute and value:
            old_value = getattr(self,self.attributes[attribute][5:])
            setattr(self,self.attributes[attribute][5:],value)
            return getattr(self,self.attributes[attribute][5:]) , old_value

        # If some attribute is missing, refer to verbose
        if any([attribute,value]) and not all([attribute,value]):
            print('Only 1 parameter has been passed to \"change_value\" func. Redirecting to input behaviour')

        print('Select attribute to change:')
        for n, attr in self.attributes.items():
            print(f'{n}: {' '.join(attr[5:].split('_')).capitalize()}')

        while True:
            try:
                choice = int(input(f'Enter a number between 1 and {len(self.attributes)}\n0 to exit\n\n'))
                if choice > len(self.attributes) or choice < 0:
                    raise ValueError
                if choice == 0:
                    return

                formatted_choice = ' '.join(str(self.attributes[choice])[5:].split('_')).capitalize()

                old_value = getattr(self,self.attributes[choice][5:])
                new_value = int(input(f'Provide a number to update \"{formatted_choice}\"\nCurrently is {old_value}\n0 to exit\n\n')) 
                if new_value < 0:
                    raise ValueError
                if new_value == 0:
                    return
                 
            except ValueError:
                print(f'Please, provide a valid number')
                continue

            break
            
        setattr(self,self.attributes[choice][5:],new_value)
        print(f'{formatted_choice} value has been changed to {new_value} (Was {old_value})')
        return getattr(self,self.attributes[choice][5:]), old_value

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

        '''print(f'Total Ahorros: {self.total_ahorros} €\nFacturas Mensual: {self.facturas_mensual} €')
        print(f'Gasto Mensual: {self.gasto_mensual} €\nSurplus Total: {self.calculate_surplus()} €')
        print(f'Media mensual: {self.calculate_monthly_surplus():.2f} €')
        print(f'Meses Restantes: {self.meses_restantes}\nUltimo Mes: {self.fecha_final.strftime("%d/%m/%Y")}')
        '''

    
class bot_excel():

    def __init__(self):
        pass



if __name__ == '__main__':
    object = bot_jona() 
    '''print(object.calculate_surplus())
    print(object.change_value(1,2574))
    print(object.change_value(2))'''

    object.display_info()

    '''
    1:'self.total_ahorros' = 2374
    2:'self.facturas_mensual' = 30
    3:'self.gasto_mensual' = 70
    '''