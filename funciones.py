# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#                           INDICE - HAY 12 FUNCIONES
#
#                 Las funciones construidas aquí tienen por objeto
#             completar un análisis de rentabilidad total (renta fija)
#                       quien se sintetiza en la función 12. 
#
#
# FUNCION 1: Línea 103. 
#            Nombre: tasabadlar
#            Descripción: Construye serie de tasa badlar esperada por REM del BCRA.
#
# FUNCION 2: Línea 167. 
#            Nombre: ffbonocap
#            Descripción: Construye el flujo de fondos de un activo de renta fija,
#                         hasta la fecha horizonte. Este activo debe ser o cupon 
#                         cero, bullet, o uno que paga capital y renta al vencimiento. 
#
# FUNCION 3: Línea 365. 
#            Nombre: ffbonodesc
#            Descripción: Construye el flujo de fondos de un activo de renta fija,
#                         luego de la fecha horizonte. Este activo debe ser o 
#                         cupon cero, bullet, o uno que paga capital y renta al 
#                         vencimiento. 
#
# FUNCION 4: Línea 564. 
#            Nombre: capflujos
#            Descripción: Capitaliza los flujos cobrados del bono hasta la fecha 
#                         de horizonte de inversión.
#
# FUNCION 5: Línea 700. 
#            Nombre: grafica_bonos
#            Descripción: Realiza la gráfica de dispersión de renta fija soberana 
#                         en pesos, en pesos CER, en pesos dólar linked, y en USD.
#                         También grafica las líneas de regresión simple correspondeintes. 
#
# FUNCION 6: Línea 831. 
#            Nombre: tabla_infla
#            Descripción: Realiza un dataframe con la inflación mensual esperada.
#                         La serie se extiende por una cantidad de meses que se 
#                         debe indicar. Para realizar la estimación, se utiliza 
#                         el mercado de renta fija en pesos y en pesos CER.
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (CER de diciembre).  
#
# FUNCION 7: Línea 1030. 
#            Nombre: tabla_dev
#            Descripción: Crea un DataFrame con la tasa de devaluación/depreciación 
#                         mensual esperada y también la acumulada correspondiente.
#                         La tasa de dev/dep se obtiene de una de tres fuentes:
#                         1) bonos USD versus bonos CER, 2) bonos en DL vs bonos 
#                         en pesos, y 3) futuros.
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (tca3500 de diciembre). 
#
# FUNCION 8: Línea 1227. 
#            Nombre: tabla_infla_esc
#            Descripción: Crea un DataFrame que contiene la serie de inflación
#                         esperada "arbitraria", es decir, es un escenario imagi-
#                         nado en función de un nivel base de inflación mensual y 
#                         una tasa de variación de este nivel en puntos porcen-
#                         tuales. 
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (CER de diciembre). 
#
# FUNCION 9: Línea 1373. 
#            Nombre: tabla_dev_esc
#            Descripción: Crea un DataFrame que contiene la serie de dev/dep
#                         esperada "arbitraria", es decir, es un escenario imagi-
#                         nado en función de un nivel base de dev/dep mensual y 
#                         una tasa de variación de este nivel en puntos porcentuales. 
#            Aclaración:  Esta función debe actualizar todos los años sus últimas
#                         líneas de código (tca3500 de diciembre).  
#
# FUNCION 10: Línea 1561.  
#             Nombre: flujobono_act 
#             Descripción: Genera el flujo de fondos actualizado de renta fija 
#                          hasta la fecha horizonte. Utilizando el flujo de fondos
#                          base, se aplica el índice CER o la tasa de dev/dep 
#                          segun corresponda. 
#    
# FUNCION 11: Línea 1758. 
#             Nombre: p_reventa 
#             Descripción: Genera el precio de reventa esperado de un activo de
#                          renta fija. Este precio se obtiene para la fecha hori-
#                          zonte.
#    
# FUNCION 12: Línea 1971.
#             Nombre: analisis_rt 
#             Descripción: Genera una tabla con todos los ticket de los bonos 
#                          bullet y las letras en pesos, pesos CER, y pesos DL,
#                          y para cada una se muestra su rendimiento total anual
#                          esperado, y los motivos que lo generan: cobro de cupones,
#                          cobro de intereses por reinversión, y cobro por reventa
#                          o por cobro de capital.   
# 
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 1
    
def tasabadlar(directorio, nombre_archivo):
    """
    Esta funcion genera un dataframe con las tasas badlar mensuales esperadas.
    La base de datos que utiliza es el REM, por ello, los únicos argumentos son  
    la ubicacion del archivo y su nombre (del que se descarga del BCRA). 
    
    """
    from datetime import datetime
    import pandas as pd

    # Descargamos el archivo de tasa badlar del REM, es un excel, y le cambiamos 
    # el nombre. Luego lo importamos:
    badlar=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',
                         sheet_name='Resultados TOP 10',header=31,
                         usecols='B:D',nrows=8)

    # Cambiamos las fechas, reemplazando su día 30 o 31 por el primero de cada 
    # mes.
    for i in range(6):
        badlar.loc[i,'Período']=datetime(badlar.loc[i,'Período'].year,
                                     badlar.loc[i,'Período'].month,1)

    # Deducimos las tasas, asumiendo que la tasa de los próximos 12 meses es un 
    # promedio.
    badlar.Promedio=badlar.Promedio*30/365/100
    badlar['acumulado']=(badlar.Promedio+1).cumprod()
    badlar.set_index('Período',inplace=True)
    tasa_deducida=((badlar.Promedio[-2]+1)**(365/30)/badlar.acumulado[-3])**(1/6)-1
    tasa_estimada=badlar.Promedio[-2]

    # Creamos la nueva tabla. Paso 1/2:
    tasas=badlar.Promedio
    tasas=pd.DataFrame(tasas)
    tasas=tasas.drop(index=[tasas.index[-1],'próx. 12 meses'],axis=0)

    # Creamos la nueva tabla. Paso 2/2:
    nuevas_fechas=[]

    for i in range(1,7):
        if tasas.index[-1].month+i<=12:
            f=f'{tasas.index[-1].year}-{tasas.index[-1].month+i}-01'
            f=datetime.strptime(f,'%Y-%m-%d')
            nuevas_fechas.append(f)
        else:
            g=f'{tasas.index[-1].year+1}-{tasas.index[-1].month+i-12}-01'
            g=datetime.strptime(g,'%Y-%m-%d')
            nuevas_fechas.append(g)
            
    nuevas_fechas=pd.DataFrame(nuevas_fechas)
    nuevas_fechas.columns=['fechas']
    nuevas_fechas['Promedio']=tasa_deducida
    nuevas_fechas.iloc[-1,1]=tasa_estimada
    nuevas_fechas.set_index('fechas',inplace=True)

    # Unimos los dos dataframes.
    tasas=pd.concat([tasas,nuevas_fechas],axis=0)
    tasas=tasas.rename(columns={'Promedio':'tasas_badlar'})
    
    return tasas

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 2

def ffbonocap(cupon1,cupon2,f_vencimiento,f_horizonte,t_cupon,tipo,
                  c_cupones,vn=100):
    """
    Función útil para obtener el flujo de fondos hasta la fecha horizonte de 
    un bono cupón cero, bonos bullet, o incluso un bono que paga sólo un cupón
    junto con el capital.  
    Adminte que la fecha de vencimiento y la fecha donde se paga el último cupon
    no coincidan. Tambien admite que la fecha horizonte y de vencimiento no 
    coincidan.
    
    PARAMETROS
    ----------
    cupon1: Es un string, obligatorio.
    Descripción: Es el mes y día de pago del primer cupón de cada año, por 
    ejemplo: 05-09.
        
    cupon2: Es un string, obligatorio.
    Descripción: Es el mes y día de pago del segundo cupón de cada año, por 
    ejemplo: 11-09.
        
    f_vencimiento: Es un string, obligatorio.
    Descripción: Es el año, mes, y día donde vence completamente el bono. Por 
    ejemplo: 2026-11-09.
        
    f_horizonte: Es un string, obligatorio.
    Descripción: Es el año, mes, y día donde se venderá el bono para salir de 
    la posición comprada, es la fecha del horizonte de inversión. Por ejemplo: 
    2024-03-01.
        
    t_cupon: float, obligatorio.
    Descripción: es la tasa del cupon anual y en porcentaje, por ejemplo, 8.
    
    tipo: String, obligatorio.
    Descripción: Es el tipo de bono. Puede ser 'bullet' o 'letra'. Los bonos que
    amortizan capital y cuentan con otras condiciones, se deben importar de excel.
    
    c_cupones: Integer, obligatorio.
    Descripción: Los valores relevantes son 0 (cero) y 1 (uno). Este parámetro 
    indica si la letra paga o no paga renta. Cuando sí lo hace su valor es 1 y 
    el pago se entiende es realizado junto con el capital. Cuando no paga renta,
    la letra es un cupón cero.    
    
    vn: integer, opcional.
    Descripción: es el valor nominal del bono, por defecto es de 100.
    Resulta importante notar que este parámetro también puede interpretarse como
    cantidad de valores nominales adquiridos, por ende, su valor puede calcularse
    como el monto de dinero invertido dividido el precio de compra y multiplicado
    por el valor nominal. 

    RESULTADO
    -------
    flujo_bis : DataFrame
    Descripción: Esta función devuelve el flujo de fondos del bono -cupon, 
    capital, y flujo total-, indicando las fechas que se corresponden con cada
    pago/cobro, y ajustando el flujo de fondos de acuerdo al horizonte de inver-
    sión. En particular, devuelve el flujo de fondos que se encuentra antes de 
    la fecha horizonte.

    """
    from datetime import datetime
    import pandas as pd
    import collections

    f_vencimiento=datetime.strptime(f_vencimiento,'%Y-%m-%d')
    f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')
    # A partir del tipo de bono se define el flujo de fondos.
    if tipo=='bullet':
        ahora=datetime.now()
        ahora=datetime(ahora.year,ahora.month,ahora.day)

        # Transformamos la fecha de vencimiento y horizonte (año, mes, y dia) en
        # tipo datetime. Y creamos la lista que contendrá las fechas de pago.
        flujo=[ahora]

        # El siguiente bucle instala las fechas de pago de cupones y capital.
        for i in range(f_vencimiento.year-ahora.year+1):
             años=i+ahora.year
             f1=f'{años}-{cupon1}'
             f1=datetime.strptime(f1,'%Y-%m-%d')
             flujo.append(f1)
             f2=f'{años}-{cupon2}'
             f2=datetime.strptime(f2,'%Y-%m-%d')
             flujo.append(f2)
        
        # Se crea el DataFrame y se toma la máscara correspondiente. También se crea
        # una columna para que identifique estas fechas como fechas que pagan cupones.
        flujo=pd.DataFrame(flujo)    
        flujo.columns=['fecha'] 
        flujo['tipo']='cupon'       
        flujo=flujo.loc[(flujo.fecha>=ahora) & (flujo.fecha<=f_vencimiento)]
        
        # Ahora incorporamos la fecha de vencimiento sólo si es mayor a la fecha 
        # de pago del último cupón, en caso contrario, el código no se modifica.
        if f_vencimiento>flujo.iloc[-1,0]:
            f_venc=[]
            f_venc.append(f_vencimiento)
            f_venc=pd.DataFrame(f_venc)
            f_venc.columns=['fecha']
            f_venc['tipo']='capital'
            flujo=pd.concat([flujo,f_venc],axis=0)
        elif f_vencimiento==flujo.iloc[-1,0]:
            flujo.iloc[-1,1]='cupon+capital'      
                
        flujo.set_index('fecha',inplace=True)    

        # Creamos copia de flujo como auxiliar para utilizar en las siguientes
        # líneas. Este 'flujo2' cuenta con fecha de cupones y de capital.
        flujo2=flujo
     
        # Colocamos la fecha horizonte y las columnas de cupones y saldo, pero 
        # sin valores.
        if collections.Counter(f_horizonte==flujo2.index)[True]==1:
            flujo['cupones']=0
            flujo['saldo']=0  
        else:
            f_hor=[]
            f_hor.append(f_horizonte)
            f_hor=pd.DataFrame(f_hor)
            f_hor.columns=['fecha']
            f_hor['tipo']='nada'
            f_hor.set_index('fecha',inplace=True)
            flujo=pd.concat([flujo,f_hor],axis=0)
            flujo=flujo.sort_values('fecha',ascending=True)
            flujo['cupones']=0
            flujo['saldo']=0  

        # Ahora creamos el flujo de pago de cupones. 
        for i in range(len(flujo.index)):
            if (flujo.iloc[i,0]=='cupon') or (flujo.iloc[i,0]=='cupon+capital'):
                flujo.iloc[i,1]=vn*t_cupon/200

        # Ahora creamos el flujo de pago de saldo bullet.         
        for i in range(len(flujo.index)):
            if (flujo.iloc[i,0]=='capital') or (flujo.iloc[i,0]=='cupon+capital'):
                flujo.iloc[i,2]=vn

        # La fecha actual debe tener un pago igual a cero.
        flujo.iloc[0]=0
                  
        # Se finaliza creando el flujo de fondos total y eliminando la columna 'tipo'.
        flujo['flujo_total']=flujo.cupones+flujo.saldo
        flujo.drop('tipo',axis=1,inplace=True)
     
        # Ahora generamos la máscara que contiene fechas menores e iguales a la 
        # fecha horizonte.
        flujo_bis=flujo.loc[flujo.index<=f_horizonte] 
        
    elif tipo=='letra':
        # Transformamos la fecha actual, de vencimiento, y de horizonte (año, mes,
        # y dia) en tipo datetime. También creamos la lista que las contendrá.
        ahora=datetime.now()
        ahora=datetime(ahora.year,ahora.month,ahora.day)
        flujo=[ahora,f_vencimiento] 
        
        # Se arma el DataFrame con estas fechas, junto con las columnas 'cupones' 
        # y 'saldo' para mantener la estructura requerida.   
        flujo=pd.DataFrame(flujo)
        flujo.columns=['fecha']
        flujo['cupones']=0
        flujo['saldo']=0
        flujo.set_index('fecha',inplace=True)
      
        # Se incorpora el valor del saldo y la columna de 'flujo_total'.
        if c_cupones==0:
            flujo.loc[f_vencimiento,'saldo']=vn
            flujo['flujo_total']=flujo.cupones+flujo.saldo
        elif c_cupones==1:
            flujo.loc[f_vencimiento,'cupones']=vn*t_cupon/100
            flujo.loc[f_vencimiento,'saldo']=vn
            flujo['flujo_total']=flujo.cupones+flujo.saldo
         
        # Incorporamos la fecha horizonte.
        if f_horizonte!=f_vencimiento:
            f_hor=[]
            f_hor.append(f_horizonte)
            f_hor=pd.DataFrame(f_hor)
            f_hor.columns=['fecha']
            f_hor['cupones']=0
            f_hor['saldo']=0
            f_hor['flujo_total']=0
            f_hor.set_index('fecha',inplace=True)
            flujo=pd.concat([flujo,f_hor],axis=0)
            flujo.sort_index(ascending=True,inplace=True)
           
        # Ahora generamos la máscara que contiene fechas menores e iguales a la 
        # fecha horizonte.
        flujo_bis=flujo.loc[flujo.index<=f_horizonte]
        
    else:
        flujo_bis='El parámetro tipo es -bullet- o -letra- no hay otra opcion'
        
    return flujo_bis

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 3

def ffbonodesc(cupon1,cupon2,f_vencimiento,f_horizonte,t_cupon,tipo,
                   c_cupones,vn=100):
    """
    Función útil para obtener el flujo de fondos posterior a la fecha de horizonte
    de un bono cupón cero, bonos bullet, o incluso un bono que paga sólo un cupón
    y lo hace junto con el capital.  
    Adminte que la fecha de vencimiento y la fecha donde se paga el último cupon
    no coincidan.
    Admite que la fecha horizonte y de vencimiento no coincidan.
    
    PARAMETROS
    ----------
    cupon1: Es un string, obligatorio.
    Descripción: Es el mes y día de pago del primer cupón de cada año, por 
    ejemplo: 05-09.
        
    cupon2: Es un string, obligatorio.
    Descripción: Es el mes y día de pago del segundo cupón de cada año, por 
    ejemplo: 11-09.
        
    f_vencimiento: Es un string, obligatorio.
    Descripción: Es el año, mes, y día donde vence completamente el bono. Por 
    ejemplo: 2026-11-09.
        
    f_horizonte: Es un string, obligatorio.
    Descripción: Es el año, mes, y día donde se venderá el bono para salir de 
    la posición comprada, es la fecha del horizonte de inversión. Por ejemplo: 
    2024-03-01.
        
    t_cupon: float, obligatorio.
    Descripción: es la tasa del cupon anual y en porcentaje, por ejemplo, 8.
    
    tipo: String, obligatorio.
    Descripción: Es el tipo de bono. Puede ser 'bullet' o 'letra'. Los bonos que
    amortizan capital y cuentan con otras condiciones, se deben importar de excel.
    
    c_cupones: Integer, obligatorio.
    Descripción: Los valores relevantes son 0 (cero) y 1 (uno). Este parámetro 
    indica si la letra paga o no paga renta. Cuando sí lo hace su valor es 1 y 
    el pago se entiende es realizado junto con el capital. Cuando no paga renta,
    la letra es un cupón cero.    
    
    vn: integer, opcional.
    Descripción: es el valor nominal del bono, por defecto es de 100.
    Resulta importante notar que, este parámetro también puede interpretarse como
    cantidad de valores nominales adquiridos, por ende, su valor puede calcularse
    como el monto de dinero invertido dividido el precio de compra y multiplicado
    por el valor nominal. 

    RESULTADO
    -------
    flujo_bis2 : DataFrame
    Descripción: Esta función devuelve el flujo de fondos del bono -cupon, 
    capital, y flujo total-, indicando las fechas que se corresponden con cada
    pago/cobro, y ajustando el flujo de fondos de acuerdo al horizonte de inver-
    sión. En particular, el flujo que devuelve es el posterior a la fecha hori-
    zonte, el cual será útil cuando debamos descontar para obtener el precio fu-
    turo de reventa del bono en cuestión.

    """
    from datetime import datetime
    import pandas as pd
    import collections

    f_vencimiento=datetime.strptime(f_vencimiento,'%Y-%m-%d')
    f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')
    # A partir del tipo de bono se define el flujo de fondos.
    if tipo=='bullet':
        ahora=datetime.now()
        ahora=datetime(ahora.year,ahora.month,ahora.day)

        # Transformamos la fecha de vencimiento y horizonte (año, mes, y dia) en
        # tipo datetime. Y creamos la lista que contendrá las fechas de pago.
        flujo=[ahora]

        # El siguiente bucle instala las fechas de pago de cupones y capital.
        for i in range(f_vencimiento.year-ahora.year+1):
             años=i+ahora.year
             f1=f'{años}-{cupon1}'
             f1=datetime.strptime(f1,'%Y-%m-%d')
             flujo.append(f1)
             f2=f'{años}-{cupon2}'
             f2=datetime.strptime(f2,'%Y-%m-%d')
             flujo.append(f2)
        
        # Se crea el DataFrame y se toma la máscara correspondiente. También se crea
        # una columna para que identifique estas fechas como fechas que pagan cupones.
        flujo=pd.DataFrame(flujo)    
        flujo.columns=['fecha'] 
        flujo['tipo']='cupon'       
        flujo=flujo.loc[(flujo.fecha>=ahora) & (flujo.fecha<=f_vencimiento)]
        
        # Ahora incorporamos la fecha de vencimiento sólo si es mayor a la fecha 
        # de pago del último cupón, en caso contrario, el código no se modifica.
        if f_vencimiento>flujo.iloc[-1,0]:
            f_venc=[]
            f_venc.append(f_vencimiento)
            f_venc=pd.DataFrame(f_venc)
            f_venc.columns=['fecha']
            f_venc['tipo']='capital'
            flujo=pd.concat([flujo,f_venc],axis=0)
        elif f_vencimiento==flujo.iloc[-1,0]:
            flujo.iloc[-1,1]='cupon+capital'      
                
        flujo.set_index('fecha',inplace=True)    

        # Creamos copia de flujo como auxiliar para utilizar en las siguientes
        # líneas. Este 'flujo2' cuenta con fecha de cupones y de capital.
        flujo2=flujo
     
        # Colocamos la fecha horizonte y las columnas de cupones y saldo, pero 
        # sin valores.
        if collections.Counter(f_horizonte==flujo2.index)[True]==1:
            flujo['cupones']=0
            flujo['saldo']=0  
        else:
            f_hor=[]
            f_hor.append(f_horizonte)
            f_hor=pd.DataFrame(f_hor)
            f_hor.columns=['fecha']
            f_hor['tipo']='nada'
            f_hor.set_index('fecha',inplace=True)
            flujo=pd.concat([flujo,f_hor],axis=0)
            flujo=flujo.sort_values('fecha',ascending=True)
            flujo['cupones']=0
            flujo['saldo']=0  

        # Ahora creamos el flujo de pago de cupones. 
        for i in range(len(flujo.index)):
            if (flujo.iloc[i,0]=='cupon') or (flujo.iloc[i,0]=='cupon+capital'):
                flujo.iloc[i,1]=vn*t_cupon/200

        # Ahora creamos el flujo de pago de saldo bullet.         
        for i in range(len(flujo.index)):
            if (flujo.iloc[i,0]=='capital') or (flujo.iloc[i,0]=='cupon+capital'):
                flujo.iloc[i,2]=vn

        # La fecha actual debe tener un pago igual a cero.
        flujo.iloc[0]=0
                  
        # Se finaliza creando el flujo de fondos total y eliminando la columna 'tipo'.
        flujo['flujo_total']=flujo.cupones+flujo.saldo
        flujo.drop('tipo',axis=1,inplace=True)
     
        # Ahora generamos la máscara que contiene fechas menores e iguales a la 
        # fecha horizonte.
        flujo_bis=flujo.loc[flujo.index>=f_horizonte] 
        
    elif tipo=='letra':
        # Transformamos la fecha actual, de vencimiento, y de horizonte (año, mes,
        # y dia) en tipo datetime. También creamos la lista que las contendrá.
        ahora=datetime.now()
        ahora=datetime(ahora.year,ahora.month,ahora.day)
        flujo=[ahora,f_vencimiento] 
        
        # Se arma el DataFrame con estas fechas, junto con las columnas 'cupones' 
        # y 'saldo' para mantener la estructura requerida.   
        flujo=pd.DataFrame(flujo)
        flujo.columns=['fecha']
        flujo['cupones']=0
        flujo['saldo']=0
        flujo.set_index('fecha',inplace=True)
      
        # Se incorpora el valor del saldo y la columna de 'flujo_total'.
        if c_cupones==0:
            flujo.loc[f_vencimiento,'saldo']=vn
            flujo['flujo_total']=flujo.cupones+flujo.saldo
        elif c_cupones==1:
            flujo.loc[f_vencimiento,'cupones']=vn*t_cupon/100
            flujo.loc[f_vencimiento,'saldo']=vn
            flujo['flujo_total']=flujo.cupones+flujo.saldo
         
        # Incorporamos la fecha horizonte.
        if f_horizonte!=f_vencimiento:
            f_hor=[]
            f_hor.append(f_horizonte)
            f_hor=pd.DataFrame(f_hor)
            f_hor.columns=['fecha']
            f_hor['cupones']=0
            f_hor['saldo']=0
            f_hor['flujo_total']=0
            f_hor.set_index('fecha',inplace=True)
            flujo=pd.concat([flujo,f_hor],axis=0)
            flujo.sort_index(ascending=True,inplace=True)
           
        # Ahora generamos la máscara que contiene fechas menores e iguales a la 
        # fecha horizonte.
        flujo_bis=flujo.loc[flujo.index>=f_horizonte]
        
    else:
        flujo_bis='El parámetro tipo es -bullet- o -letra- no hay otra opcion'  
        
    return flujo_bis

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 4

def capflujos(serie_t,f_horizonte,flujo_bb):
    """
    Esta función capitaliza los flujos del bono bullet hasta la fecha horizonte
    de inversión.
        
    PARAMETROS
    -------
    serie_t: DataFrame.
    Descripción: Es la serie de tasas mensuales esperadas para los próximos me-
    ses. Se puede obtener con la función 'tasabadlar' o por otro medio. 
        
    f_horizonte: Es un string.
    Descripción: Es el año, mes, y día donde se venderá el bono para salir de 
    la posición comprada, es la fecha del horizonte de inversión. Por ejemplo: 
    '2024-03-01'.
    
    flujo_bb: DataFrame.
    Descripción: Es la matriz con los flujos del bono bullet, cupón, capital, y
    total. Cada flujo se debe corresponder con la fecha donde se lo cobra. Se 
    puedo obtener con la función 'bonobulletcap' o a través de otro medio.
    
    RESULTADO
    -------
    flujof_bb: DataFrame.
    Descripción: Es el mismo flujo de fondos del bono bullet con una columna
    extra, cuyo contenido son los flujos cobrados y capitalizados hasta la 
    fecha horizonte.

    """
    import pandas as pd
    from datetime import datetime
    import collections

    # Para cada cupón armamos una columna donde ubicamos las tasas badlar men-
    # suales que corresponden a su fecha y a todas las fechas siguientes. Para 
    # esto utilizamos la funcion de tasabladar.
    p=[]
    p=pd.DataFrame(p)
    for i in range(1,len(flujo_bb.index)):
        f1=f'{flujo_bb.index[i].year}-{flujo_bb.index[i].month}-01'
        p[i]=serie_t.loc[serie_t.index>=datetime.strptime(f1,'%Y-%m-%d')]
    p.fillna(0,inplace=True)

    # Para continuar la serie de tasas badlar hasta la fecha horizonte, se crea 
    # otro DataFrame que contiene las fechas que están entre la última tasa 
    # badlar y la fecha horizonte.   
    p2=[]
    f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')
    for i in range(f_horizonte.year-p.index[-1].year+1):
        año=p.index[-1].year+i
        for j in range(1,13):
            mes=j
            f1=f'{año}-{mes}-01'
            f1=datetime.strptime(f1,'%Y-%m-%d')
            p2.append(f1)
    p2=pd.DataFrame(p2,columns=['fecha'])
    p2['tasas']=0
    p2.set_index('fecha',inplace=True)
    p2=p2.loc[(p2.index>p.index[-1]) & (p2.index<=f_horizonte)]

    # Concatenamos los dos DataFrame que creamos ('p' y 'p2') para obtener la 
    # serie de tasa badlar mensual esperada para cada flujo del bono bullet.
    h=pd.concat([p,p2])
    h.drop('tasas',axis=1,inplace=True)
    h.fillna(serie_t.iloc[-1,0],inplace=True)

    # Obtenemos la matriz de factores de capitalización mensual. 
    h=h+1
    h=h.loc[h.index<=f_horizonte]

    # Debemos ajustar la matriz de f de cap, 'h', convirtiendo algunos de ellos 
    # en 1, concretamnete, aquellos que están antes del cobro de flujos. 
    for j in range(1,len(flujo_bb.index)):
        q=collections.Counter(h.index<datetime.strptime(
            f'{flujo_bb.index[j].year}-{flujo_bb.index[j].month}-01','%Y-%m-%d'))[True]
        if flujo_bb.index[j]>serie_t.index[-1]: 
            for i in range(q):
                h.iloc[i,j-1]=1

    # Consiguiendo el factor de capitalización de cada flujo para todo el período 
    # de inversión, es decir, desde la fecha de cobro hasta la fecha horizonte. 
    f_cap=[]
    f_cap=pd.DataFrame(f_cap)
    for i in range(1,len(h.columns)+1):
        f_cap[i]=h[i].cumprod()

    f_cap2=[0]
    for i in range(len(h.columns)):
        f_cap2.append(f_cap.iloc[-1,i])

    # NOTA: 'f_cap2' debe corregirse para cada fecha de cobro y para la fecha 
    #        horizonte. Por ello se genera una lista cuyos elementos, a excep-
    #        ción del primero, son los factores de capitalizción mensual que 
    #        corresponden a cada fecha de cobro de cupón y capital.  
    f_cap3=[0]
    for i in range(1,len(flujo_bb.index)):
        v=h.loc[(h.index.year==flujo_bb.index[i].year) & 
                (h.index.month==flujo_bb.index[i].month)]
        f_cap3.append(v.iloc[0,0])

    # Corregimos los factores de capitalización del período de inversión.
    # Primero descontamos:
    f_cap4=[0]
    for i in range(1,len(flujo_bb.index)):
        f_cap4.append(f_cap2[i]/f_cap3[i])

    # Segundo, capitalizamos. Supondremos que los meses son de 30 días y el año 
    # de 365 días:
    f_cap5=[0]
    for i in range(1,len(flujo_bb.index)):
        f_cap5.append(f_cap4[i]*f_cap3[i]**((30-flujo_bb.index[i].day)/30))
        
    # Generamos una variable float que contiene al factor de capitalización 
    # mensual de la fecha horizonte.
    f_cap_h=f_cap3[-1]

    # Ajustamos los factores de capitalización del período de inversión, 'f_cap5',
    # descontando y capitalizando por 'f_capS_h'.
    f_cap6=[0]
    for i in range(1,len(flujo_bb.index)):
        f_cap6.append((f_cap5[i]/f_cap_h)*f_cap_h**((f_horizonte.day)/30))

    # Se aplican los factores de capitalización sobre los flujos.
    flujo_bb['f_t_futuro']=0
    for i in range(len(f_cap6)):
        flujo_bb.iloc[i,-1]=flujo_bb.iloc[i,-2]*f_cap6[i]
    
    flujof_bb=flujo_bb
    
    return flujof_bb

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 5
   
def grafica_bonos(fecha,directorio,nombre_archivo):
    """
    Genera las gráficas que permiten conocer la posición de cada uno de los 
    instrumentos de renta fija soberana en pesos y en pesos CER disponibles en 
    el mercado argentino, junto con la curva en pesos y en pesos CER (regresión). 
    Estas gráficas se ubican en el mapa TIR-DM.
    
    Para que la función arroje un resultado, debe utilizarse un archivo excel 
    en donde se cargan regularmente los ticket, DM, y TIR anual de estos papeles.
    Este archivo tiene un formato determinado que debe respetarse para que pueda
    utilizarse esta función.

    PARAMETROS
    ----------
    fecha: String.
    Descripción: Es la fecha que corresponde al día donde se toman los datos 
    DM y TIR anual (para pesos CER y sólo pesos). Con esta se define la pestaña
    del excel de donde se toman los datos. 
    Por ejemplo, '13-01-23'.
    
    directorio: String.
    Descripción: Es la carpeta o ubicacion donde se encuentra guardado el archivo
    excel con datos de bonos u ONs
    
    nombre_archivo: String.
    Descripción: Es el nombre del archivo excel con datos de bonos u ONs
    
    
    RESULTADO
    -------
    La función no tiene return, pero sí genera un resultado, el cual debe
    guardarse en alguna variable al llamar la función, de este modo se podrán
    ver las gráficas si se imprime la variable.

    """
    
    import pandas as pd
    import matplotlib.pyplot as plt
    from statsmodels.formula.api import ols
    import numpy as np
    
    fecha_cer=f'{fecha} CER'
    fecha_pesos=f'{fecha} Pesos'
    fecha_dl=f'{fecha} DL'
    fecha_usd=f'{fecha} USD'
    
    # Importamos las series de TIR y DM de renta fija CER y en pesos.
    curva_cer=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_cer)
    curva_pesos=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_pesos)
    curva_dl=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_dl)
    curva_usd=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_usd)

    # Realizamos la regresión OLS con logaritmo neperiano sobre el regresor.
    reg_cer=ols('TIR_anual ~ np.log(DMdias)', data=curva_cer).fit()
    reg_pesos=ols('TIR_anual ~ np.log(DMdias)', data=curva_pesos).fit()
    reg_dl=ols('TIR_anual ~ np.log(DMdias)', data=curva_dl).fit()
    reg_usd=ols('TIR_anual ~ np.log(DMdias)', data=curva_usd).fit()

    # Obtenemos los valores medios/predichos, quienes serán usados en las 
    # gráficas.
    pred_cer=reg_cer.predict()
    pred_cer=pd.DataFrame(pred_cer)
    pred_cer.columns=['TIR_anual']
    pred_cer['DMdias']=curva_cer.DMdias
    pred_cer.sort_values('DMdias',inplace=True)

    pred_pesos=reg_pesos.predict()
    pred_pesos=pd.DataFrame(pred_pesos)
    pred_pesos.columns=['TIR_anual']
    pred_pesos['DMdias']=curva_pesos.DMdias
    pred_pesos.sort_values('DMdias',inplace=True)
        
    pred_dl=reg_dl.predict()
    pred_dl=pd.DataFrame(pred_dl)
    pred_dl.columns=['TIR_anual']
    pred_dl['DMdias']=curva_dl.DMdias
    pred_dl.sort_values('DMdias',inplace=True)
        
    pred_usd=reg_usd.predict()
    pred_usd=pd.DataFrame(pred_usd)
    pred_usd.columns=['TIR_anual']
    pred_usd['DMdias']=curva_usd.DMdias
    pred_usd.sort_values('DMdias',inplace=True)

    # Realizamos las gráficas de dispersión y de regresión de ambas series.
    fig, ax = plt.subplots(4,figsize=(15,15))
    ax[0].set_title('Bonos en Pesos CER:'+fecha_cer[:8])
    ax[0].scatter(curva_cer.iloc[:,-1],curva_cer.iloc[:,-2]*100,cmap='Curva CER')
    ax[0].plot(pred_cer.DMdias,pred_cer.TIR_anual*100,label='Reg bonos CER')
    ax[0].set_xlabel('Modified Duration (anualizado)')
    ax[0].set_ylabel('TIR Anual')
    for i,label in enumerate(curva_cer.ticket):
        ax[0].annotate(label,(curva_cer.iloc[:,-1][i], 
                                         curva_cer.iloc[:,-2][i]*100))
    ax[0].grid()    
             
    ax[1].set_title('Bonos en Pesos:'+fecha_pesos[:8])
    ax[1].scatter(curva_pesos.iloc[:,-1],curva_pesos.iloc[:,-2]*100,
                  cmap='Curva Pesos', label='Bonos en pesos')
    ax[1].plot(pred_pesos.DMdias,pred_pesos.TIR_anual*100,
               label='Reg bonos en pesos')
    ax[1].set_xlabel('Modified Duration (anualizado)')
    ax[1].set_ylabel('TIR Anual')
    for i,label in enumerate(curva_pesos.ticket):
        ax[1].annotate(label,(curva_pesos.iloc[:,-1][i], 
                                         curva_pesos.iloc[:,-2][i]*100))
    ax[1].grid()
    
    ax[2].set_title('Bonos DL:'+fecha_dl[:8])
    ax[2].scatter(curva_dl.iloc[:,-1],curva_dl.iloc[:,-2]*100,
                  cmap='Curva Dólar Linked', label='Bonos DL')
    ax[2].plot(pred_dl.DMdias,pred_dl.TIR_anual*100,
               label='Reg bonos DL')
    ax[2].set_xlabel('Modified Duration (anualizado)')
    ax[2].set_ylabel('TIR Anual')
    for i,label in enumerate(curva_dl.ticket):
        ax[2].annotate(label,(curva_dl.iloc[:,-1][i], 
                                         curva_dl.iloc[:,-2][i]*100))
    ax[2].grid()
    
    ax[3].set_title('Bonos USD:'+fecha_usd[:8])
    ax[3].scatter(curva_usd.iloc[:,-1],curva_usd.iloc[:,-2]*100,
                  cmap='Curva Soberana en USD', label='Bonos USD')
    ax[3].plot(pred_usd.DMdias,pred_usd.TIR_anual*100,
               label='Reg bonos USD')
    ax[3].set_xlabel('Modified Duration (anualizado)')
    ax[3].set_ylabel('TIR Anual')
    for i,label in enumerate(curva_usd.ticket):
        ax[3].annotate(label,(curva_usd.iloc[:,-1][i], 
                                         curva_usd.iloc[:,-2][i]*100))
    ax[3].grid()
    
    fig.subplots_adjust(hspace=0.3)

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 6

def tabla_infla(fecha1,directorio,nombre_archivo,cant_meses=6):
    """
    Crea un DataFrame que permite conocer la inflación mensual esperada. Dicho 
    resultado se obtiene a partir de los precios de los bonos que cotizan en 
    bolsa. La inflación esperada para el mes donde se realiza la compra equiva-
    le a la inflación esperada para los días restantes de dicho mes. La infla- 
    ción mensual esperada que se genera tiene un máximo de 60 meses hacia
    delante si el mes inicial es enero (1), y 48 meses hacia delante si el mes
    inicial es diciembre (12). Se utilzian meses de 30 días y año de 360 dias. 

    PARAMETROS
    ----------  
    fecha1: String.
    Descripción: Es la fecha que corresponde al día donde se toman los datos 
    DM y TIR anual (para pesos CER y sólo pesos). Con esta se define la pestaña
    del excel de donde se toman los datos. 
    Por ejemplo, '17-01-23'.
    
    directorio: String.
    Descripción: Es la carpeta o ubicacion donde se encuentra guardado el archivo
    excel con datos de bonos u ONs.
    
    nombre_archivo: String.
    Descripción: Es el nombre del archivo excel con datos de bonos u ONs.
        
    cant_meses: integer, optional
    Descripción: Es la cantidad de meses hacia delante, a partir del momento de 
    la compra de los bonos y letras, que se extiende la serie. Por defecto es 
    igual a 6.

    RESULTADO
    -------
    tabla_infla: DataFrame.
    Descripción: Es la tabla de inflación mensual esperada e inflación acumula-
    da.

    """
    import pandas as pd
    from statsmodels.formula.api import ols
    import numpy as np
    from datetime import datetime

    fecha_cer=f'{fecha1} CER'
    fecha_pesos=f'{fecha1} Pesos'
    
    # Importamos las series de TIR y DM de renta fija CER y en pesos.
    curva_cer=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_cer)
    curva_pesos=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_pesos)
    
    # Realizamos la regresión OLS con logaritmo neperiano sobre el regresor (DM)
    reg_cer=ols('TIR_anual ~ np.log(DMdias)', data=curva_cer).fit()
    reg_pesos=ols('TIR_anual ~ np.log(DMdias)', data=curva_pesos).fit()
    
    # Obtenemos el valor de los coeficientes de la regresión lineal log simple.
    inter_cer=reg_cer.params[0]
    coef_cer=reg_cer.params[1]
    inter_pesos=reg_pesos.params[0]
    coef_pesos=reg_pesos.params[1]
    
    # Construimos el DataFrame que vincula DMdias con días efectivos para un 
    # período de tiempo determinado desde el momento de la compra (máximo "cant_meses" 
    # es decir, esto se define exógenamente). Se supone año de 360 días y meses de 
    # 30 días:
    tabla_dias=[]
    for i in range(cant_meses+1):
        tabla_dias.append(i)
    tabla_dias=pd.DataFrame(tabla_dias) 
    tabla_dias.columns=['mes_desde_comp']
    tabla_dias.drop(0,inplace=True)
    
    tabla_dias['dias_desde_comp']=0
    if (datetime.now().month==2) & (datetime.now().day>=28): 
        tabla_dias.loc[1,'dias_desde_comp']=0
    elif datetime.now().day>=30:
        tabla_dias.loc[1,'dias_desde_comp']=0
    else:    
        tabla_dias.loc[1,'dias_desde_comp']=30-datetime.now().day
        
    for i in range(2,cant_meses+1):
        tabla_dias.loc[i,'dias_desde_comp']=i*30-(30-tabla_dias.loc[
            1,'dias_desde_comp'])
    tabla_dias.set_index('mes_desde_comp',inplace=True)
    tabla_dias['DMdias']=tabla_dias.dias_desde_comp/360  
    
    # Al DataFrame 'tabla_dias' incorporamos una columna TIR_anual para bonos 
    # en pesos CER y otra para bonos en pesos.  
    tabla_dias['TIR_anual_cer']=0
    tabla_dias['TIR_anual_pesos']=0
    for i in range(len(tabla_dias.index)):
        tabla_dias.iloc[i,-2]=inter_cer+coef_cer*np.log(tabla_dias.iloc[i,-3])
    for i in range(len(tabla_dias.index)):
        tabla_dias.iloc[i,-1]=inter_pesos+coef_pesos*np.log(tabla_dias.iloc[i,-3])    
    
    # Creamos la tabla de inflación mensual e inflación acumulada desde la 
    # compra. La 1era fila de la 1era columna es la inflación esperada hasta el 
    # final del mes donde se realiza la compra, el resto es la infla esperada 
    # cada 30 dias. 
    tabla_infla=[]
    for i in range(datetime.now().month,cant_meses+datetime.now().month):
        if i<=12:
            tabla_infla.append(i)
        elif i<=24:
            tabla_infla.append(i-12)
        elif i<=36:
            tabla_infla.append(i-24)
        elif i<=48:
            tabla_infla.append(i-36)    
        else:    
            tabla_infla.append(i-48)
        if i==60:
            break
      
    tabla_infla=pd.DataFrame(tabla_infla)
    tabla_infla.columns=['mes']
    tabla_infla['infla_mens']=0
    
    tabla_infla.iloc[0,1]=((1+tabla_dias.iloc[0,3])/(1+tabla_dias.iloc[0,2]))**(
        tabla_dias.iloc[0,0]/360)-1
    for i in range(1,len(tabla_infla.index)):
        tabla_infla.iloc[i,1]=((1+tabla_dias.iloc[i,3])/(1+tabla_dias.iloc[i,2]))**(
            30/360)-1
    tabla_infla['infla_acum']=(1+tabla_infla.infla_mens).cumprod()-1
    
    # Ahora introducimos la fecha (año-mes-dia) como índice de la inflación es-
    # perada. Para esto creamos un dataframe donde crearemos las fechas, del 
    # cual tomaremos su máscara con fechas iguales y posteriores a la actual, 
    # para luego concatenar este datafrema con 'tabla_infla', eliminando aque-
    # llas filas con datos inexistentes. 
    año=[]
    for i in range(5):
        i=i+1
        for j in range(1,13):
            año.append(datetime.now().year-1+i)
    
    año=pd.DataFrame(año)
    año.columns=['año']
    año['mes']=0
    
    for i in año.index:
        if i+1<=12:
            año.loc[i,'mes']=i+1
        elif i+1<=24:
            año.loc[i,'mes']=i+1-12    
        elif i+1<=36:
            año.loc[i,'mes']=i+1-24
        elif i+1<=48:
            año.loc[i,'mes']=i+1-36
        elif i+1<=60:
            año.loc[i,'mes']=i+1-48
        else:
            año.loc[i,'mes']=i+1-60
        if i==año.index[-1]:
            break
    
    año['fecha']=0
    for i in año.index:
        año1=año.loc[i,'año']
        mes1=año.loc[i,'mes']
        if mes1==2: 
            fecha=f'{año1}-{mes1}-28'
            fecha=datetime.strptime(fecha,'%Y-%m-%d')
            año.loc[i,'fecha']=fecha
        elif (mes1==4) or (mes1==6) or (mes1==9) or (mes1==11):
            fecha=f'{año1}-{mes1}-30'
            fecha=datetime.strptime(fecha,'%Y-%m-%d')
            año.loc[i,'fecha']=fecha
        else:
            fecha=f'{año1}-{mes1}-31'
            fecha=datetime.strptime(fecha,'%Y-%m-%d')
            año.loc[i,'fecha']=fecha
    
    año=año.loc[año.fecha>=datetime.now()]
    
    año['indice']=0
    for i in range(len(año.index)):
        año.iloc[i,-1]=i   
        if i==len(año.index):
            break
    año.set_index('indice',inplace=True)
    
    tabla_infla=pd.concat([tabla_infla,año],axis=1).dropna()
    tabla_infla.drop(['mes','año'],axis=1,inplace=True)
    tabla_infla.set_index('fecha',inplace=True)
    
    # INPUT: Fecha de diciembre e inflación de diciembre del año anterior al actual. 
    # ESTO DEBE ACTUALIZARSE TODOS LOS MESES.
    # No obstnate, si el mes actual no es enero, entonces la aclaración anterior no
    # corresponde, y en su lugar se debe colocar la inflación del mes anterior al 
    # actual.
    serie_cer=pd.read_excel('Serie CER.xlsx').set_index('Fecha')
    
    if datetime.now().month==1:
        mes_ant=12
        año_ant=datetime.now().year-1
        
        f_dic22_1=f'{año_ant}-{mes_ant}-01'
        f_dic22_1=datetime.strptime(f_dic22_1,'%Y-%m-%d')
        f_dic22_2=f'{año_ant}-{mes_ant}-31'
        f_dic22_2=datetime.strptime(f_dic22_2,'%Y-%m-%d')
        
        t_rem=serie_cer.loc[serie_cer.index==f_dic22_2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_dic22_1].iloc[0,0]-1
        l=[f_dic22_2,t_rem,0]
    else:
        mes_ant=datetime.now().month-1
        año_act=datetime.now().year
        
        f_mesant1=f'{año_act}-{mes_ant}-01'
        f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')   
        if mes_ant==2:   
            f_mesant2=f'{año_act}-{mes_ant}-28'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_cer.loc[serie_cer.index==f_mesant2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
        elif (mes_ant==4) or (mes_ant==6) or (mes_ant==9) or (mes_ant==11):       
            f_mesant2=f'{año_act}-{mes_ant}-30'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_cer.loc[serie_cer.index==f_mesant2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
        else: 
            f_mesant2=f'{año_act}-{mes_ant}-31'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_cer.loc[serie_cer.index==f_mesant2].iloc[0,0
                           ]/serie_cer.loc[serie_cer.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
    
    # Se crea el DataFrame que contiene la fecha de diciembre o del mes anterior, y
    # se le suma su inflación. 
    l=pd.DataFrame(l).T
    l.set_index(0,inplace=True)
    l=l.rename(columns={1:'infla_mens',2:'infla_acum'})
    
    # Se une este nuevo DataFrame con la tabla de inflación.
    tabla_infla=pd.concat([tabla_infla,l],axis=0)
    tabla_infla.sort_index(inplace=True)
    
    return tabla_infla

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 7

def tabla_dev(f_limite,fecha1,tipo,tcn_hoy,tcn_rofex,ticket_usd,ticket_cer,
              ticket_dl,ticket_pesos,directorio,nombre_archivo,nombre_archivo_tc,
              meses_adelante=6):
    """
    ¿Qué hace? Crea un DataFrame con la tasa de devaluación/depreciación mensual
    esperada y también la acumulada correspondiente. Existen tres fuentes de
    información entre las que se puede elegir: 1) bonos USD versus bonos CER, 
    2) bonos en DL vs bonos en pesos, y 3) futuros.
    
    Consejo: Antes de introducir los tickets, buscar sólo aquellos que tengan
    la misma DM.

    PARAMETROS
    ----------
    f_limite : String, obligatorio.
    Descripción: Esta determina el plazo para el que rige la tasa de devaluación/
    depreciación surgida entre el tcn A3500 actual y la cotización del dólar fu-
    turo. En otras palabras, es la cantidad de días que se coloca como denomina-
    dor en la potencia que corresponde a la tasa de inflación equivalente.
    Por ejemplo, si el contrato de futuro que miramos es de junio, entonces, 
    esta variable debe tomar el siguiente valor: '2023-06-30'.
        
    fecha1 : String, obligatorio.
    Descripción: Es la fecha que representa el nombre de la pestaña del excel
    de donde se obtienen los datos, por ejemplo, '17-01-2023'.
        
    tipo : String, obligatorio.
    Descripción: Representa la fuente de información que se usa para realizar 
    los cálculos de la tasa de dev/dep. Hay tres tipos: 1) 'usd-cer', 2) 'dl-pesos'
    y 3) 'rofex'.
        
    tcn_hoy : Float, obligatorio.
    Descripción: Es el tipo de cambio A3500 vigente en el día.
        
    tcn_rofex : Float, obligatorio.
    Descripción: Es el tipo de cambio al que cerró el contrato de futuro del 
    mes horizonte, por ejemplo, al entrar a la web del rofex se busca el contra-
    to de junio dado que estamos en enero (6 meses).
        
    ticket_usd : String, obligatorio.
    Descripción: Es el ticket del bono en dólares que tiene la misma DM que el 
    bono cer. Por ejemplo, 'AL29'.
        
    ticket_cer : String, obligatorio.
    Descripción: Es el ticket del bono en pesos cer que tiene la misma DM que el 
    bono usd. Por ejemplo, 'TX28'.
        
    ticket_dl : String, obligatorio.
    Descripción: Es el ticket del bono en dólares linked que tiene la misma DM 
    que el bono en pesos. Por ejemplo, 'TV24'.
        
    ticket_pesos : String, obligatorio.
    Descripción: Es el ticket del bono en pesos que tiene la misma DM que el 
    bono en dólares linked. Por ejemplo, 'TO26'.
    
    directorio: String.
    Descripción: Es la carpeta o ubicacion donde se encuentran guardados los 
    archivos excels con datos de bonos u ONs y con la serie del A3500.
    
    nombre_archivo: String.
    Descripción: Es el nombre del archivo excel con datos de bonos u ONs.
    
    nombre_archivo_tc: String.
    Descripción: Es el nombre del archivo excel con la serie del A3500.
        
    meses_adelante : Integer, opcional con valor por defecto igual a 6.
    Descripción: Determina la extensión o cantidad de meses que tendrá la serie 
    de tasa de dev/dep. 
        
    RESULTADO
    -------
    tabla_dev : DataFrame.
    Descripción: Es la tabla con la devaluación/depreciación mensual y acumula-
    da esperada. 

    """
           
    import pandas as pd
    from datetime import datetime, timedelta

    fecha_cer=f'{fecha1} CER'
    fecha_pesos=f'{fecha1} Pesos'
    fecha_usd=f'{fecha1} USD'
    fecha_dl=f'{fecha1} DL'
    
    # Se define el DataFrame que contendrá la tasa de devaluación/depreciación:
    año=[]
    for i in range(5):
        i=i+1
        for j in range(1,13):
            año.append(datetime.now().year-1+i)

    año=pd.DataFrame(año)
    año.columns=['año']
    año['mes']=0

    for i in año.index:
        if i+1<=12:
            año.loc[i,'mes']=i+1
        elif i+1<=24:
            año.loc[i,'mes']=i+1-12    
        elif i+1<=36:
            año.loc[i,'mes']=i+1-24
        elif i+1<=48:
            año.loc[i,'mes']=i+1-36
        elif i+1<=60:
            año.loc[i,'mes']=i+1-48
        else:
            año.loc[i,'mes']=i+1-60
        if i==año.index[-1]:
            break

    año['fecha']=0
    for i in año.index:
        año1=año.loc[i,'año']
        mes1=año.loc[i,'mes']
        if mes1==2: 
            fecha=f'{año1}-{mes1}-28'
            fecha=datetime.strptime(fecha,'%Y-%m-%d')
            año.loc[i,'fecha']=fecha
        elif (mes1==4) or (mes1==6) or (mes1==9) or (mes1==11):
            fecha=f'{año1}-{mes1}-30'
            fecha=datetime.strptime(fecha,'%Y-%m-%d')
            año.loc[i,'fecha']=fecha
        else:
            fecha=f'{año1}-{mes1}-31'
            fecha=datetime.strptime(fecha,'%Y-%m-%d')
            año.loc[i,'fecha']=fecha

    f_limite=datetime.strptime(f_limite,'%Y-%m-%d')
    base=(f_limite-datetime.now()).days
    tabla_dev=año
    tabla_dev['dev_men']=0
    tabla_dev['dev_acum']=0
    tabla_dev.set_index('fecha',inplace=True)
    tabla_dev.drop(['mes','año'],axis=1,inplace=True)
    tabla_dev=tabla_dev.loc[(tabla_dev.index>=datetime.now())].copy()

    # Se define la tasa de devaluación/depreciación:
    if tipo=='rofex':
        tabla_dev['dev_men']=(tcn_rofex/tcn_hoy)**(30/base)-1
        tabla_dev.iloc[0,0]=(1+tabla_dev.iloc[0,0])**(
            (tabla_dev.index[0].day-datetime.now().day)/tabla_dev.index[0].day)-1

        tabla_dev.dev_acum=(1+tabla_dev.dev_men).cumprod()-1
        tabla_dev=tabla_dev.loc[tabla_dev.index<=datetime.now()+timedelta(30*meses_adelante)]

    elif tipo=='usd-cer':
        infla_acum=tabla_infla(fecha1,cant_meses=12).iloc[-1,-1]
        tabla_infla1=tabla_infla(fecha1,cant_meses=12)
        potencia=tabla_infla1.index[0].day/(tabla_infla1.index[0].day-datetime.now(
            ).day)
        infla_acum=(1+infla_acum)/(1+tabla_infla1.iloc[0,0])*(
            1+tabla_infla1.iloc[0,0])**potencia-1

        b_usd=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_usd).set_index(
            'ticket')
        b_cer=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_cer).set_index(
            'ticket')
            
        tabla_dev['dev_men']=((1+b_cer.loc[ticket_cer].TIR_anual+infla_acum)/(
            1+b_usd.loc[ticket_usd].TIR_anual))**(1/12)-1
        tabla_dev.iloc[0,0]=(1+tabla_dev.iloc[0,0])**(
            (tabla_dev.index[0].day-datetime.now().day)/tabla_dev.index[0].day)-1

        tabla_dev.dev_acum=(1+tabla_dev.dev_men).cumprod()-1
        tabla_dev=tabla_dev.loc[tabla_dev.index<=datetime.now()+timedelta(30*meses_adelante)]
            
    elif tipo=='dl-pesos':
        b_pesos=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_pesos).set_index(
            'ticket')
        b_dl=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx',sheet_name=fecha_dl).set_index(
            'ticket')
            
        tabla_dev['dev_men']=((1+b_pesos.loc[ticket_pesos].TIR_anual)/(
            1+b_dl.loc[ticket_dl].TIR_anual))**(1/12)-1
        tabla_dev.iloc[0,0]=(1+tabla_dev.iloc[0,0])**(
            (tabla_dev.index[0].day-datetime.now().day)/tabla_dev.index[0].day)-1
            
        tabla_dev.dev_acum=(1+tabla_dev.dev_men).cumprod()-1
        tabla_dev=tabla_dev.loc[tabla_dev.index<=datetime.now()+timedelta(30*meses_adelante)]

    else:
        tabla_dev='Hay un error en el tipeo de la variable -tipo-'  
        
    # INPUT: Fecha de diciembre y tasa de dev/dep de diciembre del año anterior 
    # al actual. ESTO DEBE ACTUALIZARSE TODOS LOS MESES.
    # No obstante, si el mes actual no es enero, entonces la aclaración anterior
    # no corresponde, y en su lugar se debe colocar la tasa de dev/dep del mes 
    # anterior al actual.    
    serie_tca3500=pd.read_excel(f'{directorio}/{nombre_archivo_tc}.xlsx').set_index('Fecha')
    
    if datetime.now().month==1:
        mes_ant=12
        año_ant=datetime.now().year-1
        
        f_dic22_1=f'{año_ant}-{mes_ant}-02'
        f_dic22_1=datetime.strptime(f_dic22_1,'%Y-%m-%d')
        f_dic22_2=f'{año_ant}-{mes_ant}-30'
        f_dic22_2=datetime.strptime(f_dic22_2,'%Y-%m-%d')
        
        t_rem=serie_tca3500.loc[serie_tca3500.index==f_dic22_2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_dic22_1].iloc[0,0]-1
        l=[f_dic22_2,t_rem,0]
           
    else:
        mes_ant=datetime.now().month-1
        año_act=datetime.now().year
         
        if mes_ant==1:
            f_mesant1=f'{año_act}-{mes_ant}-02'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')   
            
            f_mesant2=f'{año_act}-{mes_ant}-31'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]       
        elif mes_ant==2:   
            f_mesant1=f'{año_act}-{mes_ant}-01'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')   
            
            f_mesant2=f'{año_act}-{mes_ant}-28'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]       
        elif (mes_ant==4) or (mes_ant==6) or (mes_ant==9) or (mes_ant==11): 
            f_mesant1=f'{año_act}-{mes_ant}-01'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')  
            
            f_mesant2=f'{año_act}-{mes_ant}-30'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]     
        else: 
            f_mesant1=f'{año_act}-{mes_ant}-01'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')  
            
            f_mesant2=f'{año_act}-{mes_ant}-31'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
    
    # Se crea el DataFrame que contiene la fecha de diciembre y su inflación.
    l=pd.DataFrame(l).T
    l.set_index(0,inplace=True)
    l=l.rename(columns={1:'dev_men',2:'dev_acum'})
    
    # Se une este nuevo DataFrame con la tabla de inflación.
    tabla_dev=pd.concat([tabla_dev,l],axis=0)
    tabla_dev.sort_index(inplace=True)
    
    return tabla_dev

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 8

def tabla_infla_esc(tem_base,t_var_tem,fecha1,f_horizonte,directorio,nombre_archivo_cer):
    """
    Genera un DataFrame con un escenario imaginado sobre el devenir de la infla-
    ción mensual y su acumulado. Sólo se debe establecer una base para la infla-
    ción y una tasa de variación.
    El proceso que genera la dinámica inflacionaria es lineal, determinado por 
    una base y una tasa de cambio en puntos porcentuales (que es constante).

    PARAMETROS
    ----------
    tem_base : Float.
    Descripción: Es la tasa de inflación mensual esperada para el mes actual, y 
    es la tasa que se utiliza como base, es decir, a partir de la cual se genera
    el resto de la serie. Por ejemplo: 0.05.
        
    t_var_tem : Float.
    Descripción: Son los puntos porcentuales de cambio (>0, <0, o =0) que se 
    aplican mes a mes a la base de la inflación. Es lo que explica la variación
    de la inflación mes a mes. Por ejemplo: 0.0005.

    fecha1 : String.
    Descripción: Es la fecha que representa el nombre de la pestaña del excel
    de donde se obtienen los datos, por ejemplo, '17-01-2023'. Este argumento
    permite tomar como inflación del mes corriente la calculada con el mercado
    de bonos de la función 6.
    
    f_horizonte : String.
    Descripción: Es la fecha horizonte de inversión, momento donde se venden los
    activos en cartera. Por ejemplo: 2025-11-09 (año-mes-dia).
    
    directorio: String.
    Descripción: Es la carpeta o ubicacion donde se encuentran guardados los 
    archivos excels la serie CER.
    
    nombre_archivo_cer: String.
    Descripción: Es el nombre del archivo excel con la serie CER.

    RESULTADO
    -------
    tabla_infla_esc : DataFrame.
    Descripción: Es el par de series de inflación, la primera columna contiene
    la inflación esperada mensual. La segunda columna contiene la inflación espe-
    rada acumulada mes a mes.

    """

    import pandas as pd
    from datetime import datetime

    # Creamos las fechas que posteriormente se convertirán en el índice de la 
    # tabla de inflación.
    año=[]
    for i in range(5):
        i=i+1
        for j in range(1,13):
            año.append(datetime.now().year-1+i)
        
    año=pd.DataFrame(año)
    año.columns=['año']
    año['mes']=0

    for i in año.index:
        if i+1<=12:
            año.loc[i,'mes']=i+1
        elif i+1<=24:
            año.loc[i,'mes']=i+1-12    
        elif i+1<=36:
            año.loc[i,'mes']=i+1-24
        elif i+1<=48:
            año.loc[i,'mes']=i+1-36
        elif i+1<=60:
            año.loc[i,'mes']=i+1-48
        else:
            año.loc[i,'mes']=i+1-60
        if i==año.index[-1]:
            break

    año['fecha']=0
    for i in año.index:
        año1=año.loc[i,'año']
        mes1=año.loc[i,'mes']
        if mes1==2: 
           fecha=f'{año1}-{mes1}-28'
           fecha=datetime.strptime(fecha,'%Y-%m-%d')
           año.loc[i,'fecha']=fecha
        elif (mes1==4) or (mes1==6) or (mes1==9) or (mes1==11):
           fecha=f'{año1}-{mes1}-30'
           fecha=datetime.strptime(fecha,'%Y-%m-%d')
           año.loc[i,'fecha']=fecha
        else:
           fecha=f'{año1}-{mes1}-31'
           fecha=datetime.strptime(fecha,'%Y-%m-%d')
           año.loc[i,'fecha']=fecha

    año=año.loc[año.fecha>=datetime.now()]

    # Creamos la tabla inflación para los diferentes escenarios. 
    tabla_infla_esc=año
    tabla_infla_esc['infla_mens']=0
    tabla_infla_esc['infla_acum']=0
    tabla_infla_esc.drop(['año','mes'],axis=1,inplace=True)
    tabla_infla_esc.set_index('fecha',inplace=True)

    # Ahora introducimos la inflación base y su tasa de variación (en puntos 
    # porcentuales), así podremos colocar la inflación mensual esperada.
    
    tabla_infla_esc.iloc[0,0]=tabla_infla(fecha1).iloc[1,0]
    tabla_infla_esc.iloc[1,0]=tem_base

    for i in range(2,len(tabla_infla_esc.index)):
        tabla_infla_esc.iloc[i,0]=tabla_infla_esc.iloc[i-1,0]+t_var_tem
        
    tabla_infla_esc['infla_acum']=(1+tabla_infla_esc['infla_mens']).cumprod()-1    
        
    # Recortamos la 'tabla_infla_esc' descartando las fechas posteriores a la 
    # fecha horizonte.
    f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')

    if f_horizonte.month==2:
        f_horizonte=f'{f_horizonte.year}-{f_horizonte.month}-28'
    elif (f_horizonte.month==4) or (f_horizonte.month==6) or (f_horizonte.month==9) or (
            f_horizonte.month==11):
        f_horizonte=f'{f_horizonte.year}-{f_horizonte.month}-30'
    else:
        f_horizonte=f'{f_horizonte.year}-{f_horizonte.month}-31'

    f_horizonte=datetime.strptime(f_horizonte, '%Y-%m-%d')

    tabla_infla_esc=tabla_infla_esc.loc[tabla_infla_esc.index<=f_horizonte]

    # INPUT: Fecha de diciembre e inflación de diciembre del año anterior al actual. 
    # ESTO DEBE ACTUALIZARSE TODOS LOS MESES.
    # No obstnate, si el mes actual no es enero, entonces la aclaración anterior no
    # corresponde, y en su lugar se debe colocar la inflación del mes anterior al 
    # actual.
    serie_cer=pd.read_excel(f'{directorio}/{nombre_archivo_cer}.xlsx').set_index('Fecha')
    
    if datetime.now().month==1:
        mes_ant=12
        año_ant=datetime.now().year-1
        
        f_dic22_1=f'{año_ant}-{mes_ant}-01'
        f_dic22_1=datetime.strptime(f_dic22_1,'%Y-%m-%d')
        f_dic22_2=f'{año_ant}-{mes_ant}-31'
        f_dic22_2=datetime.strptime(f_dic22_2,'%Y-%m-%d')
        
        t_rem=serie_cer.loc[serie_cer.index==f_dic22_2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_dic22_1].iloc[0,0]-1
        l=[f_dic22_2,t_rem,0]
    else:
        mes_ant=datetime.now().month-1
        año_act=datetime.now().year
        
        f_mesant1=f'{año_act}-{mes_ant}-01'
        f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')   
        if mes_ant==2:   
            f_mesant2=f'{año_act}-{mes_ant}-28'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_cer.loc[serie_cer.index==f_mesant2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
        elif (mes_ant==4) or (mes_ant==6) or (mes_ant==9) or (mes_ant==11):       
            f_mesant2=f'{año_act}-{mes_ant}-30'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_cer.loc[serie_cer.index==f_mesant2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
        else: 
            f_mesant2=f'{año_act}-{mes_ant}-31'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_cer.loc[serie_cer.index==f_mesant2].iloc[0,0
                            ]/serie_cer.loc[serie_cer.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
    
    # Se crea el DataFrame que contiene la fecha de diciembre o del mes anterior, y
    # se le suma su inflación. 
    l=pd.DataFrame(l).T
    l.set_index(0,inplace=True)
    l=l.rename(columns={1:'infla_mens',2:'infla_acum'})
    
    # Se une este nuevo DataFrame con la tabla de inflación.
    tabla_infla_esc=pd.concat([tabla_infla_esc,l],axis=0)
    tabla_infla_esc.sort_index(inplace=True)
    
    return tabla_infla_esc

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 9

def tabla_dev_esc(t_tc_base,var_t_tc,f_horizonte,f_limite,fecha1,tipo,tcn_hoy,
                  tcn_rofex,ticket_usd,ticket_cer,ticket_dl,ticket_pesos,
                  directorio,nombre_archivo_tc,meses_adelante=6):
    """
    Genera un DataFrame con un escenario imaginado sobre el devenir de la de-
    valuación/depreciación. Sólo se debe establecer una base para y una tasa de 
    variación.
    El proceso que genera la dinámica de dev/dep es lineal, determinado por 
    una base y una tasa de cambio en puntos porcentuales (que es constante).

    PARAMETROS
    ----------
    t_tc_base : Float, obligatorio.
    Descripción: Es la tasa de dep/dev mensual esperada para el mes actual, y 
    es la tasa que se utiliza como base, es decir, a partir de la cual se genera
    el resto de la serie. Por ejemplo: 0.05.
        
    var_t_tc : Float, obligatorio.
    Descripción: Son los puntos porcentuales de cambio (>0, <0, o =0) que se 
    aplican mes a mes a la base de la dep/dev. Es lo que explica la variación
    de la dev/dep mes a mes. Por ejemplo: 0.0005.
        
    f_horizonte : String, obligatorio.
    Descripción: Es la fecha horizonte de inversión, momento donde se venden los
    activos en cartera. Por ejemplo: 2025-11-09 (año-mes-dia).
    
    f_limite : String, obligatorio.
    Descripción: Es una fecha que determina el plazo para el que rige la tasa de 
    devaluación/depreciación surgida entre el tcn A3500 actual y la cotización 
    del dólar futuro. En otras palabras, es la cantidad de días que se coloca 
    como denominador en la potencia que corresponde a la tasa de inflación 
    equivalente. Por ejemplo, si el contrato de futuro que miramos es de junio, 
    entonces, esta variable debe tomar el siguiente valor: '2023-06-30'.
        
    fecha1 : String, obligatorio.
    Descripción: Es la fecha que representa el nombre de la pestaña del excel
    de donde se obtienen los datos, por ejemplo, '17-01-2023'.
        
    tipo : String, obligatorio.
    Descripción: Representa la fuente de información que se usa para realizar 
    los cálculos de la tasa de dev/dep. Hay tres tipos: 1) 'usd-cer', 2) 'dl-pesos'
    y 3) 'rofex'.
        
    tcn_hoy : Float, obligatorio.
    Descripción: Es el tipo de cambio A3500 vigente en el día.
        
    tcn_rofex : Float, obligatorio.
    Descripción: Es el tipo de cambio al que cerró el contrato de futuro del 
    mes horizonte, por ejemplo, al entrar a la web del rofex se busca el contra-
    to de junio dado que estamos en enero (6 meses).
        
    ticket_usd : String, obligatorio.
    Descripción: Es el ticket del bono en dólares que tiene la misma DM que el 
    bono cer. Por ejemplo, 'AL29'.
        
    ticket_cer : String, obligatorio.
    Descripción: Es el ticket del bono en pesos cer que tiene la misma DM que el 
    bono usd. Por ejemplo, 'TX28'.
        
    ticket_dl : String, obligatorio.
    Descripción: Es el ticket del bono en dólares linked que tiene la misma DM 
    que el bono en pesos. Por ejemplo, 'TV24'.
        
    ticket_pesos : String, obligatorio.
    Descripción: Es el ticket del bono en pesos que tiene la misma DM que el 
    bono en dólares linked. Por ejemplo, 'TO26'.
        
    meses_adelante : Integer, opcional con valor por defecto igual a 6.
    Descripción: Determina la extensión o cantidad de meses que tendrá la serie 
    de tasa de dev/dep. 
    
    directorio: String.
    Descripción: Es la carpeta o ubicacion donde se encuentran guardados los 
    archivos excels con datos de bonos u ONs y con la serie del A3500.

    nombre_archivo_tc: String.
    Descripción: Es el nombre del archivo excel con la serie del A3500.

    RESULTADO
    -------
    tabla_dev_esc : DataFrame.
    Descripción: Es el par de series de dep/dev, la primera columna contiene
    la dep/dev esperada mensual. La segunda columna contiene la dep/dev espe-
    rada acumulada mes a mes.

    """
    
    import pandas as pd
    from datetime import datetime

    # Creamos las fechas que posteriormente se convertirán en el índice de la tabla
    # de inflación.
    año=[]
    for i in range(5):
        i=i+1
        for j in range(1,13):
            año.append(datetime.now().year-1+i)

    año=pd.DataFrame(año)
    año.columns=['año']
    año['mes']=0

    for i in año.index:
        if i+1<=12:
            año.loc[i,'mes']=i+1
        elif i+1<=24:
            año.loc[i,'mes']=i+1-12    
        elif i+1<=36:
            año.loc[i,'mes']=i+1-24
        elif i+1<=48:
            año.loc[i,'mes']=i+1-36
        elif i+1<=60:
            año.loc[i,'mes']=i+1-48
        else:
            año.loc[i,'mes']=i+1-60
        if i==año.index[-1]:
            break

    año['fecha']=0
    for i in año.index:
        año1=año.loc[i,'año']
        mes1=año.loc[i,'mes']
        if mes1==2: 
           fecha=f'{año1}-{mes1}-28'
           fecha=datetime.strptime(fecha,'%Y-%m-%d')
           año.loc[i,'fecha']=fecha
        elif (mes1==4) or (mes1==6) or (mes1==9) or (mes1==11):
           fecha=f'{año1}-{mes1}-30'
           fecha=datetime.strptime(fecha,'%Y-%m-%d')
           año.loc[i,'fecha']=fecha
        else:
           fecha=f'{año1}-{mes1}-31'
           fecha=datetime.strptime(fecha,'%Y-%m-%d')
           año.loc[i,'fecha']=fecha

    año=año.loc[año.fecha>=datetime.now()]

    # Creamos la tabla inflación para los diferentes escenarios. 
    tabla_dev_esc=año
    tabla_dev_esc['dev_men']=0
    tabla_dev_esc['dev_acum']=0
    tabla_dev_esc.drop(['año','mes'],axis=1,inplace=True)
    tabla_dev_esc.set_index('fecha',inplace=True)

    # Ahora introducimos la inflación base y su tasa de variación (en puntos porcen-
    # tuales), así podremos colocar la inflación mensual esperada. 
    tabla_dev_esc.iloc[0,0]=tabla_dev(f_limite,fecha1,tipo,tcn_hoy,tcn_rofex,
                                      ticket_usd,ticket_cer,ticket_dl,ticket_pesos,
                                      meses_adelante).iloc[1,0]
    tabla_dev_esc.iloc[1,0]=t_tc_base

    for i in range(2,len(tabla_dev_esc.index)):
        tabla_dev_esc.iloc[i,0]=tabla_dev_esc.iloc[i-1,0]+var_t_tc
        
    tabla_dev_esc['dev_acum']=(1+tabla_dev_esc['dev_men']).cumprod()-1    
          
    # Recortamos la 'tabla_infla_esc' descartando las fechas posteriores a la fecha
    # horizonte.
    f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')

    if f_horizonte.month==2:
        f_horizonte=f'{f_horizonte.year}-{f_horizonte.month}-28'
    elif (f_horizonte.month==4) or (f_horizonte.month==6) or (f_horizonte.month==9) or (
            f_horizonte.month==11):
        f_horizonte=f'{f_horizonte.year}-{f_horizonte.month}-30'
    else:
        f_horizonte=f'{f_horizonte.year}-{f_horizonte.month}-31'

    f_horizonte=datetime.strptime(f_horizonte, '%Y-%m-%d')

    tabla_dev_esc=tabla_dev_esc.loc[tabla_dev_esc.index<=f_horizonte]

    # INPUT: Fecha de diciembre y tasa de dev/dep de diciembre del año anterior 
    # al actual. ESTO DEBE ACTUALIZARSE TODOS LOS MESES.
    # No obstante, si el mes actual no es enero, entonces la aclaración anterior
    # no corresponde, y en su lugar se debe colocar la tasa de dev/dep del mes 
    # anterior al actual.    
    serie_tca3500=pd.read_excel(f'{directorio}/{nombre_archivo_tc}.xlsx').set_index('Fecha')
    
    if datetime.now().month==1:
        mes_ant=12
        año_ant=datetime.now().year-1
        
        f_dic22_1=f'{año_ant}-{mes_ant}-02'
        f_dic22_1=datetime.strptime(f_dic22_1,'%Y-%m-%d')
        f_dic22_2=f'{año_ant}-{mes_ant}-30'
        f_dic22_2=datetime.strptime(f_dic22_2,'%Y-%m-%d')
        
        t_rem=serie_tca3500.loc[serie_tca3500.index==f_dic22_2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_dic22_1].iloc[0,0]-1
        l=[f_dic22_2,t_rem,0]
           
    else:
        mes_ant=datetime.now().month-1
        año_act=datetime.now().year
         
        if mes_ant==1:
            f_mesant1=f'{año_act}-{mes_ant}-02'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')   
            
            f_mesant2=f'{año_act}-{mes_ant}-31'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]       
        elif mes_ant==2:   
            f_mesant1=f'{año_act}-{mes_ant}-01'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')   
            
            f_mesant2=f'{año_act}-{mes_ant}-28'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]       
        elif (mes_ant==4) or (mes_ant==6) or (mes_ant==9) or (mes_ant==11): 
            f_mesant1=f'{año_act}-{mes_ant}-01'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')  
            
            f_mesant2=f'{año_act}-{mes_ant}-30'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]     
        else: 
            f_mesant1=f'{año_act}-{mes_ant}-01'
            f_mesant1=datetime.strptime(f_mesant1,'%Y-%m-%d')  
            
            f_mesant2=f'{año_act}-{mes_ant}-31'
            f_mesant2=datetime.strptime(f_mesant2,'%Y-%m-%d')
            
            t_rem=serie_tca3500.loc[serie_tca3500.index==f_mesant2].iloc[0,0
                ]/serie_tca3500.loc[serie_tca3500.index==f_mesant1].iloc[0,0]-1
            l=[f_mesant2,t_rem,0]
    
    # Se crea el DataFrame que contiene la fecha de diciembre y su inflación.
    l=pd.DataFrame(l).T
    l.set_index(0,inplace=True)
    l=l.rename(columns={1:'dev_men',2:'dev_acum'})
    
    # Se une este nuevo DataFrame con la tabla de inflación.
    tabla_dev_esc=pd.concat([tabla_dev_esc,l],axis=0)
    tabla_dev_esc.sort_index(inplace=True)

    return tabla_dev_esc    

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 10

def flujobono_act(tabla_inflaa,tabla_deva,ticket,f_horizonte,i_cer_hoy,tcn_hoy,
                  directorio, nombre_archivo, vn=100):
    """
    Esta función modifica el flujo de fondos del bono, actualizando su saldo de 
    acuerdo al índice correspondiente (CER o TCA3500). Si el bono no debe actua-
    lizarse, la función devuelve el flujo común, como lo hace la función número
    dos (2). 
    Esta función admite el uso de tablas de inflación y devaluación/depreciación
    creadas arbitrariamente o utilizando las funciones hechas en esta librería.
    No obstante, estas tablas siempre deben tener el mismo formato que las generadas
    por las funciones correspondientes de esta librería. 

    PARAMETROS
    ----------
    tabla_inflaa : DataFrame, obligatorio.
    Descripción: Es la tabla de inflación esperada, construida con las funciones
    hechas en esta librería o importada de excel u otro programa. 
        
    tabla_deva : DataFrame, obligatorio.
    Descripción: Es la tabla de dev/dep esperada, construida con las funciones
    hechas en esta librería o importada de excel u otro programa. 
        
    ticket : String, obligatorio.
    Descripción: Es el ticket/nombre del bono a analizar. Por ejemplo TV24.
        
    f_horizonte : String, obligatorio.
    Descripción: Es la fecha horizonte de inversión.
        
    i_cer_hoy : Float, obligatorio.
    Descripción: Es el valor actual del índice CER, se obtiene en la web del BCRA. 
        
    tcn_hoy : Float, obligatorio.
    Descripción: Es el valor actual del tipo de cambio mayorista, resolución
    A3500. Se obtiene en la web del BCRA.
    
    directorio: String.
    Descripción: Es la carpeta o ubicacion donde se encuentra guardado el 
    archivo excel con datos sobre bonos y ONs.

    nombre_archivo_tc: String.
    Descripción: Es el nombre del archivo excel con datos sobre bonos y ONs.
    
    vn : float, opcional.
    Descripción: Es el valor nominal del bono. Por defecto se encuentra en 100. 
    Este valor puede cambiarse a capricho, e incluso hacerlo depender del monto de 
    inversión para obtener la cantidad de valores nominales comprados dado el precio 
    de compra y el valor nominal mínimo (monto invertido*valor nominal / precio).

    RESULTADO
    -------
    flujo_bb : DataFrame.
    Descripción: Es el flujo de fondos del bono actualizada por inflación o dep/dev
    esperada. 

    """
    
    import pandas as pd
    from datetime import datetime

    # Obtenemos los inputs. Primero fijamos el ticket y la fecha horizonte, impor-
    # tamos el excel sobre características de los bonos, y luego obtenemos el flujo
    # de fondos dividios el índice CER de la fecha de emisión.
    bonos=pd.read_excel(f'{directorio}/{nombre_archivo}.xlsx').set_index('Ticket')
    flujo_bb=ffbonocap(bonos.cupon1.loc[ticket],bonos.cupon2.loc[ticket],
                           bonos.f_vencimiento.loc[ticket],f_horizonte,
                           bonos.tasa_cupon_anual.loc[ticket],
                           bonos.tipo_bono1.loc[ticket],bonos.tipo_bono3[ticket],vn)

    # Obtenemos el flujo de fondos del bono bullet ajustado por la inflación 
    # esperada o depreciación esperada.
    if bonos.tipo_bono2.loc[ticket]=='CER':
        # Se ajusta el flujo con el índice CER que corresponde a la fecha de 
        # emisión.
        flujo_bb=flujo_bb/bonos.indice_inicial.loc[ticket]

        # Se acualiza el índice CER de hoy y se lo ajusta para tener en cuenta la 
        # fecha de cobro y que sea de 10 días antes de dicha fecha. 
        for i in range(1,len(flujo_bb.index)):
            #Primera etapa: ajuste con el índice en bruto.
            tasa_infla_acum=tabla_inflaa.loc[
                (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                (tabla_inflaa.index.month==flujo_bb.index[i].month)].iloc[0,-1]
            i_cer_act=i_cer_hoy*(1+tasa_infla_acum)
                
            # Segunda etapa: ajuste del índice.    
            if flujo_bb.index[i].day-10>=0:
                tasa_infla=tabla_inflaa.loc[
                       (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                       (tabla_inflaa.index.month==flujo_bb.index[i].month)].iloc[0,0]
                potencia=(flujo_bb.index[i].day-10)/tabla_inflaa.loc[
                     (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                     (tabla_inflaa.index.month==flujo_bb.index[i].month)].index.day[0]
                
                i_cer_act=(i_cer_act/(1+tasa_infla))*(1+tasa_infla)**potencia
                              
                flujo_bb.iloc[i]=flujo_bb.iloc[i]*i_cer_act
                    
            elif (flujo_bb.index[i].day-10<0) & (flujo_bb.index[i].month==1):   
                tasa_infla1=tabla_inflaa.loc[
                       (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                       (tabla_inflaa.index.month==flujo_bb.index[i].month)].iloc[0,0]
                tasa_infla2=tabla_inflaa.loc[
                       (tabla_inflaa.index.year==flujo_bb.index[i].year-1)&
                       (tabla_inflaa.index.month==12)].iloc[0,0]
                
                # Como nos vamos al mes de diciembre del "año anterior", la 
                # cantidad máxima de días es siempre 31.            
                dias=31+(flujo_bb.index[i].day-10)            
                base=31
                
                potencia=dias/base
                
                i_cer_act=(i_cer_act/((1+tasa_infla2)*(1+tasa_infla1)))*(
                                                            1+tasa_infla2)**potencia
                                 
                flujo_bb.iloc[i]=flujo_bb.iloc[i]*i_cer_act               

            else: 
                tasa_infla1=tabla_inflaa.loc[
                       (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                       (tabla_inflaa.index.month==flujo_bb.index[i].month)].iloc[0,0]
                tasa_infla2=tabla_inflaa.loc[
                       (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                       (tabla_inflaa.index.month==flujo_bb.index[i].month-1)].iloc[0,0]

                fecha1=tabla_inflaa.loc[
                       (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                       (tabla_inflaa.index.month==flujo_bb.index[i].month)].index[0]
                mascara=tabla_inflaa.loc[tabla_inflaa.index<=fecha1]
                dias=mascara.index[-2].day            
                
                potencia=(dias+(flujo_bb.index[i].day-10))/tabla_inflaa.loc[
                     (tabla_inflaa.index.year==flujo_bb.index[i].year)&
                     (tabla_inflaa.index.month==flujo_bb.index[i].month-1)].index.day[0]
                i_cer_act=(i_cer_act/((1+tasa_infla2)*(1+tasa_infla1)))*(1+tasa_infla2)**potencia
                                 
                flujo_bb.iloc[i]=flujo_bb.iloc[i]*i_cer_act      

    elif bonos.tipo_bono2.loc[ticket]=='DL':
        # Este proceso de actualización se realiza en dos etapas, siempre respe-
        # tando que el tca3500 debe ser el de 3 días antes de la fecha de cobro.    
        # Etapa uno: Aplicación del tcA3500 en bruto.   
        for i in range(1,len(flujo_bb.index)):
            tasa_act_acum=1+tabla_deva.loc[(tabla_deva.index.month==flujo_bb.index[i].month)&
                            (tabla_deva.index.year==flujo_bb.index[i].year)].iloc[0,1]
            flujo_bb.iloc[i,:]=flujo_bb.iloc[i,:]*tcn_hoy*tasa_act_acum
            
        # Etapa dos: ajuste del tcA3500.
            if flujo_bb.index[i].day-3>=0:   
                tasa_act_men=1+tabla_deva.loc[
                            (tabla_deva.index.month==flujo_bb.index[i].month)&
                            (tabla_deva.index.year==flujo_bb.index[i].year)].iloc[0,0]
                potencia=(flujo_bb.index[i].day-3)/tabla_deva.loc[
                        (tabla_deva.index.year==flujo_bb.index[i].year)&
                        (tabla_deva.index.month==flujo_bb.index[i].month)].index.day[0]
            
                flujo_bb.iloc[i,:]=(flujo_bb.iloc[i,:]/tasa_act_men
                                                            )*tasa_act_men**potencia
         
            elif (flujo_bb.index[i].day-3<0) & (flujo_bb.index[i].month==1):
                tasa_act_men1=1+tabla_deva.loc[
                            (tabla_deva.index.month==flujo_bb.index[i].month)&
                            (tabla_deva.index.year==flujo_bb.index[i].year)].iloc[0,0]
                tasa_act_men2=1+tabla_deva.loc[
                            (tabla_deva.index.month==12)&
                            (tabla_deva.index.year==flujo_bb.index[i].year-1)].iloc[0,0]
              
                # Como nos vamos al mes de diciembre del "año anterior", la 
                # cantidad máxima de días es siempre 31.
                dias=31+(flujo_bb.index[i].day-3)
                base=31
               
                potencia=dias/base

                flujo_bb.iloc[i,:]=(flujo_bb.iloc[i,:]/(tasa_act_men1*tasa_act_men2)
                                                            )*tasa_act_men2**potencia
                
            else:
                tasa_act_men1=1+tabla_deva.loc[
                            (tabla_deva.index.month==flujo_bb.index[i].month)&
                            (tabla_deva.index.year==flujo_bb.index[i].year)].iloc[0,0]
                tasa_act_men2=1+tabla_deva.loc[
                            (tabla_deva.index.month==flujo_bb.index[i].month-1)&
                            (tabla_deva.index.year==flujo_bb.index[i].year)].iloc[0,0]

                mascara_dias=tabla_deva.loc[
                    (tabla_deva.index.year==flujo_bb.index[i].year)&
                    (tabla_deva.index.month==flujo_bb.index[i].month-1)].index.day[0]
                dias=mascara_dias+(flujo_bb.index[i].day-3)
                base=tabla_deva.loc[
                    (tabla_deva.index.year==flujo_bb.index[i].year)&
                    (tabla_deva.index.month==flujo_bb.index[i].month-1)].index.day[0]
                
                potencia=dias/base

                flujo_bb.iloc[i,:]=(flujo_bb.iloc[i,:]/(tasa_act_men1*tasa_act_men2)
                                                            )*tasa_act_men2**potencia
    
    return flujo_bb

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 11

def p_reventa(tabla_fb,tabla_inflaa,tabla_devaa,fecha1,f_horizonte,tipo,
              i_cer_hoy,tc_hoy,ticket):
    """
    Esta función permite obtener el precio de venta esperado del bono de interés.
    Dicho precio se obtiene utilizando la curva de rendimiento.

    PARAMETROS
    ----------
    tabla_fb : DataFrame, obligatorio.
    Descripción: Es el flujo de fondos esperado del bono, pero el que se encuentra
    más allá de la fecha de horizonte. 
        
    tabla_inflaa : DataFrame, obligatorio.
    Descripción: Es la serie de inflación mensual y acumulada esperada.
        
    tabla_devaa : DataFrame, obligatorio.
    Descripción: Es la serie de dev/dep mensual y acumulada esperada.
        
    fecha1 : String, obligatorio.
    Descripción: Es la fecha que corresponde a la pestaña del excel donde está 
    la información sobre la TIR y la DM de cada bono. Por ejemplo: '17-01-23'.
        
    f_horizonte : String, obligatorio.
    Descripción: Es la fecha que actúa como horizonte de inversión. Por ejemplo,
    '2024-06-15'.
        
    tipo : String, obligatorio.
    Descripción: Es el tipo de renta fija CER, DL, o pesos.
        
    i_cer_hoy : Float, obligatorio.
    Descripción: Es el índice CER actual.
        
    tc_hoy : Float, obligatorio.
    Descripción: Es el tipo de cambio mayorista (A3500) de hoy.
    
    ticket : String, obligatorio
    Descripción: Es el nombre del bono o letra sobre la que se quiere obtener 
    el precio de reventa.

    RESULTADO
    -------
    precio_vta : Float.
    Descripción: Es es precio de venta esperado del bono/letra de interés.

    """
    
    import pandas as pd 
    from datetime import datetime
    from statsmodels.formula.api import ols
    import numpy as np

    # Fecha actual.
    hoy=datetime.now()

    # Comienzan los cálculos previos
    fecha_cer=f'{fecha1} CER'
    fecha_pesos=f'{fecha1} Pesos'
    fecha_dl=f'{fecha1} DL'

    # Se lee el excel que contiene las condiciones sustanciales de los bonos.
    bonoss=pd.read_excel('Bonoscaracteristicas.xlsx').set_index('Ticket')

    # Importamos las series de TIR y DM de renta fija CER y en pesos.
    curva_cer=pd.read_excel('Bonoscurvas.xlsx',sheet_name=fecha_cer)
    curva_pesos=pd.read_excel('Bonoscurvas.xlsx',sheet_name=fecha_pesos)
    curva_dl=pd.read_excel('Bonoscurvas.xlsx',sheet_name=fecha_dl)

    # Realizamos la regresión OLS con logaritmo neperiano sobre el regresor (DM)
    reg_cer=ols('TIR_anual ~ np.log(DMdias)', data=curva_cer).fit()
    reg_pesos=ols('TIR_anual ~ np.log(DMdias)', data=curva_pesos).fit()
    reg_dl=ols('TIR_anual ~ np.log(DMdias)', data=curva_dl).fit()

    # Obtenemos el valor de los coeficientes de la regresión lineal log simple.
    inter_cer=reg_cer.params[0]
    coef_cer=reg_cer.params[1]

    inter_pesos=reg_pesos.params[0]
    coef_pesos=reg_pesos.params[1]

    inter_dl=reg_dl.params[0]
    coef_dl=reg_dl.params[1]

    # A partir de aquí se aplica los cálculos para obtener el precio de reventa 
    # según corresponda.
    if (tipo=='CER') or (tipo=='DUAL-CER'):
        # Actualizamos y aplicamos el índice CER sobre el flujo de fondos, junto con 
        # el índice CER de la fecha de emisión.
        f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')
        i_cer_emi=bonoss.indice_inicial.loc[ticket]

        f_act_cer=tabla_inflaa.loc[(tabla_inflaa.index.year==f_horizonte.year) & (
                                    tabla_inflaa.index.month==f_horizonte.month)
                                                                        ].iloc[0,-1]
        if tipo=='DUAL-CER':
            tabla_fb_act=(tabla_fb*i_cer_hoy*(1+f_act_cer)*bonoss.tc_inicial.loc[ticket]
                                                                      )/i_cer_emi
        else:
            tabla_fb_act=(tabla_fb*i_cer_hoy*(1+f_act_cer))/i_cer_emi

        # Construimos la tabla de tasas forward. Creamos las columnas: 
        tabla_tf=tabla_fb_act
        tabla_tf=tabla_tf.rename(columns={'cupones':'dm_dias','saldo':'tir_anual',
                                          'flujo_total':'t_efectiva'})
        tabla_tf['t_forward']=0
        tabla_tf['t_cupon_cero']=0
        tabla_tf.iloc[0:,0:]=0

        # Construimos la tabla de tasas forward. Damos valores a las celdas:
        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,0]=((tabla_tf.index[i]-hoy).days)/365

        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,1]=inter_cer+coef_cer*np.log(tabla_tf.iloc[i,0])

        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,2]=(1+tabla_tf.iloc[i,1])**(tabla_tf.iloc[i,0])-1

        for i in range(1,len(tabla_tf.index)):
            tabla_tf.iloc[i,3]=(1+tabla_tf.iloc[i,2])/(1+tabla_tf.iloc[i-1,2])-1

        tabla_tf['t_cupon_cero']=(1+tabla_tf['t_forward']).cumprod()-1

        # Obtenemos el precio de reventa esperado descontando el flujo de fondos que 
        # está más allá de la fecha de horizonte, y lo descontamos hasta la fecha 
        # horizonte.
        precio_vta=0
        f_desc=0
        for i in range(1,len(tabla_tf.index)):
            f_desc=tabla_fb_act.iloc[i,2]/(1+tabla_tf.iloc[i,4])
            precio_vta=precio_vta+f_desc

    elif tipo=='pesos':
        # Construimos la tabla de tasas forward. Creamos las columnas: 
        tabla_tf=tabla_fb
        tabla_tf=tabla_tf.rename(columns={'cupones':'dm_dias','saldo':'tir_anual',
                                          'flujo_total':'t_efectiva'})
        tabla_tf['t_forward']=0
        tabla_tf['t_cupon_cero']=0
        tabla_tf.iloc[0:,0:]=0

        # Construimos la tabla de tasas forward. Damos valores a las celdas:
        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,0]=((tabla_tf.index[i]-hoy).days)/365
            
        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,1]=inter_pesos+coef_pesos*np.log(tabla_tf.iloc[i,0])    
            
        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,2]=(1+tabla_tf.iloc[i,1])**(tabla_tf.iloc[i,0])-1

        for i in range(1,len(tabla_tf.index)):
            tabla_tf.iloc[i,3]=(1+tabla_tf.iloc[i,2])/(1+tabla_tf.iloc[i-1,2])-1

        tabla_tf['t_cupon_cero']=(1+tabla_tf['t_forward']).cumprod()-1    

        # Obtenemos el precio de reventa esperado descontando el flujo de fondos que 
        # está más allá de la fecha de horizonte, y lo descontamos hasta la fecha 
        # horizonte.
        precio_vta=0
        f_desc=0
        for i in range(1,len(tabla_tf.index)):
            f_desc=tabla_fb.iloc[i,2]/(1+tabla_tf.iloc[i,4])
            precio_vta=precio_vta+f_desc

    elif tipo=='DL':
        # Aplicamos el TCN3500 actual y su tasa de dep/dev correspondiente a la fecha
        # de emisión.
        f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')

        f_act_tc=tabla_devaa.loc[(tabla_devaa.index.year==f_horizonte.year) & (
                                    tabla_devaa.index.month==f_horizonte.month)
                                                                        ].iloc[0,-1]
        tabla_fb_act=tabla_fb*tc_hoy*(1+f_act_tc)

        # Construimos la tabla de tasas forward. Creamos las columnas: 
        tabla_tf=tabla_fb_act
        tabla_tf=tabla_tf.rename(columns={'cupones':'dm_dias','saldo':'tir_anual',
                                          'flujo_total':'t_efectiva'})
        tabla_tf['t_forward']=0
        tabla_tf['t_cupon_cero']=0
        tabla_tf.iloc[0:,0:]=0        
      
        # Construimos la tabla de tasas forward. Damos valores a las celdas:
        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,0]=((tabla_tf.index[i]-hoy).days)/365

        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,1]=inter_dl+coef_dl*np.log(tabla_tf.iloc[i,0])

        for i in range(len(tabla_tf.index)):
            tabla_tf.iloc[i,2]=(1+tabla_tf.iloc[i,1])**(tabla_tf.iloc[i,0])-1

        for i in range(1,len(tabla_tf.index)):
            tabla_tf.iloc[i,3]=(1+tabla_tf.iloc[i,2])/(1+tabla_tf.iloc[i-1,2])-1

        tabla_tf['t_cupon_cero']=(1+tabla_tf['t_forward']).cumprod()-1

        # Obtenemos el precio de reventa esperado descontando el flujo de fondos que 
        # está más allá de la fecha de horizonte, y lo descontamos hasta la fecha 
        # horizonte.
        precio_vta=0
        f_desc=0
        for i in range(1,len(tabla_tf.index)):
            f_desc=tabla_fb_act.iloc[i,2]/(1+tabla_tf.iloc[i,4])
            precio_vta=precio_vta+f_desc
            
    return precio_vta
     
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#                                   FUNCION 12

def analisis_rt(infla_tabla,deva_tabla,int_tabla,f_horizonte,i_cer_hoy,tcn_hoy,
                fecha1,monto_invertido=50_000):
    """
    ¿Qué hace esta función? Construye la tabla de análisis de rendimiento total
    esperado de cada uno de los bonos bullet que cotizan en el mercado (letras y
    bonos en pesos, en pesos CER, y en pesos dólar linked), y lo hace para una 
    fecha horizonte determinada. Este rendimiento total esperado se desagrega
    entre cobro de cupones, intereses ganados por reinversión, y cobro del capital
    o por reventa del bono/letra.

    PARAMETROS
    ----------
    infla_tabla : DataFrame, obligatorio.
    Descripción: Es una tabla con la serie de inflación mensual esperada hasta 
    cierta fecha determinada por el analista. Además, también debe contar con 
    la serie de inflación acumulada. Se puede obtener utilizando la función 6 u 8
    de esta librería, o creando una en excel e importándola (pero debe tener el 
    mismo formato que las creadas con aquellas funciones).
        
    deva_tabla : DataFrame, obligatorio.
    Descripción: Es una tabla con la serie de depreciación/devaluación mensual 
    esperada hasta cierta fecha determinada por el analista. Además, también debe 
    contar con la serie de inflación acumulada. Se puede obtener utilizando la función 
    7 o 9 de esta librería, o creando una en excel e importándola (pero debe tener 
    el mismo formato que las creadas con aquellas funciones).
        
    int_tabla : DataFrame, obligatorio.
    Descripción: Es la tabla con las tasas de interés badlar esperadas para los 
    próximos 12 meses. Se puede obtener con utilizando la función 1 de esta librería.
        
    f_horizonte : String, obligatorio.
    Descripción: Es la fecha de horizonte de inversión, donde se venden los activos
    que conforman la cartera.
        
    i_cer_hoy : Float, obligatorio.
    Descripción: Es el valor actual del índice CER, publicado por el BCRA.
        
    tcn_hoy : Float, obligatorio.
    Descripción: Es el valor actual del tipo de cambio mayorista de la resolución
    A3500 publicado por el BCRA.
        
    fecha1 : String, obligatorio.
    Descripción: Es la fecha de la pestaña del Excel llamado 'Bonoscurvas' donde
    figuran los bonos y letras en pesos, pesos CER, pesos DL, y en USD. El formato
    de esta fecha se aprecia con el siguiente ejemplo: '17-01-23' (día, mes, año).
        
    monto_invertido : Integer o Float, opcional
    Descripción: Es la cantidad de dinero utilizada para comprar el bono/letra. 
    Por defecto es de 50_000.

    RESULTADO
    -------
    tabla_definitiva : DataFrame.
    Descripción: Es la tabla con todos los ticket de los bonos bullet y letras,
    tanto en pesos, pesos CER, como en Pesos DL. Para cada ticket se muestra su 
    rendimiento total esperado anual, que corresponde al plazo constituido por 
    la fecha horizonte, y la dinámica esperada de la inflación, devaluación, y 
    las tasas de interés. Además, también permite desagregar dicho rendimiento 
    entre sus causas inmediatas: cobre de cupones, cobro de intereses por reinversión,
    y cobro por reventa del bono/letra o por cobro del capital.

    """
    
    import pandas as pd
    from datetime import datetime, timedelta

    # A partir de aquí comienza la funcion.
    bonoss=pd.read_excel('Bonoscaracteristicas.xlsx').set_index('Ticket')
    ahora=datetime.now()

    # Se crea la tabla que contendrá la información que estamos queriendo calcular.
    tabla_final=[0]
    tabla_final=pd.DataFrame(tabla_final)
    tabla_final.columns=['Ticket']
    tabla_final['RT_Anual_Esp']=0
    tabla_final['Cupones']=0
    tabla_final['Int_Reinv']=0
    tabla_final['Capital_o_Reventa']=0
    tabla_final['DUAL']=0

    for i in bonoss.index:
        ticket=i
        
        # Calculamos los valores de interés.
        if (bonoss.tipo_bono1.loc[ticket]=='bullet') or (bonoss.tipo_bono1.loc[ticket]=='letra'):
                vn=monto_invertido/bonoss.precio.loc[ticket]*100

                # Actualizamos el flujo base si corresponde por ser CER o DL.
                flujo_act=flujobono_act(tabla_inflaa=infla_tabla,tabla_deva=deva_tabla,
                                        ticket=ticket,f_horizonte=f_horizonte,
                                        i_cer_hoy=i_cer_hoy,tcn_hoy=tcn_hoy,vn=vn)           
                
                # # Capitalizamos el flujo de fondos. 
                flujo_cap=capflujos(serie_t=int_tabla,f_horizonte=f_horizonte,flujo_bb=flujo_act)
                
                # Calculamos lo cobrado en concepto de cupones, capital e intereses 
                # por reinversión.
                total_cupones=flujo_cap.cupones.sum()
                capital=flujo_cap.saldo.sum()
                int_reinv=flujo_cap.f_t_futuro.sum()-(total_cupones+capital)
                
                # Calculamos el precio de reventa.
                flujo2=ffbonodesc(cupon1=bonoss.cupon1.loc[ticket],
                                  cupon2=bonoss.cupon2.loc[ticket],
                                  f_vencimiento=bonoss.f_vencimiento.loc[ticket],
                                  f_horizonte=f_horizonte,
                                  t_cupon=bonoss.tasa_cupon_anual.loc[ticket],
                                  tipo=bonoss.tipo_bono1.loc[ticket],
                                  c_cupones=bonoss.tipo_bono3.loc[ticket],
                                  vn=vn)

                p_reventaa=p_reventa(tabla_fb=flujo2, tabla_inflaa=infla_tabla, 
                                  tabla_devaa=deva_tabla,fecha1=fecha1,
                                  f_horizonte=f_horizonte,
                                  tipo=bonoss.tipo_bono2.loc[ticket], 
                                  i_cer_hoy=i_cer_hoy,  
                                  tc_hoy=tcn_hoy,
                                  ticket=ticket)

                f_horizonte=datetime.strptime(f_horizonte,'%Y-%m-%d')
                f_vencimiento=datetime.strptime(bonoss.f_vencimiento.loc[ticket],'%Y-%m-%d')

                if f_horizonte>=f_vencimiento:
                    cap_o_reventa=capital
                else:
                    cap_o_reventa=p_reventaa

                # Se calcula la rentabilidad total.
                rent_total=(total_cupones+int_reinv+cap_o_reventa)/monto_invertido-1
                
                # Anualizamos la rentabilidad total.
                rent_total=(1+rent_total)**(365/((f_horizonte-ahora).days))-1

                # Se arma el DataFrame donde se coloca esta información.
                total_ganado=total_cupones+int_reinv+cap_o_reventa

                tabla_casi_final=[rent_total,total_cupones/total_ganado,int_reinv/total_ganado,
                          cap_o_reventa/total_ganado]
                
                tabla_casi_final=pd.DataFrame(tabla_casi_final)
                tabla_casi_final=round(tabla_casi_final.T*100,2)
                tabla_casi_final['Ticket']=ticket
                tabla_casi_final.set_index('Ticket',inplace=True)
                tabla_casi_final.reset_index(inplace=True)
                tabla_casi_final=tabla_casi_final.rename(columns={0:'RT_Anual_Esp',1:'Cupones',
                                                          2:'Int_Reinv',3:'Capital_o_Reventa'})
                
                f_horizonte=datetime.strftime(f_horizonte,'%Y-%m-%d')
                tabla_final=pd.concat([tabla_casi_final,tabla_final],axis=0)

    # Ordenamos la tabla
    tabla_final.set_index('Ticket',inplace=True)
    tabla_final.drop(0,axis=0,inplace=True)

    # Ahora trabajamos para elimianr los bonos duales con el menor rendimiento.
    # Primero: Se crea una columna que identifica si el bono es o no es DUAL.
    for i in tabla_final.index:
        tabla_final.loc[i,'DUAL']=bonoss.DUAL.loc[i]

    # Segundo: Se divide la tabla final entre bonos duales y bonos no duales usando 
    # máscaras.
    tabla_final_p1=tabla_final.loc[tabla_final.DUAL=='no'].copy()
    tabla_final_p2=tabla_final.loc[tabla_final.DUAL=='si'].copy()

    # Tercero: Se crea una columna que asigna valores a cada uno de los bonos duales,
    # por más que se repitan. 
    tabla_final_p2['igual1']=0

    for i in range(len(tabla_final_p2.index)):
        tabla_final_p2.iloc[i,-1]=i

    # Cuarto: Se crea una columna que asignará el mismo valor a los bonos duales que 
    # sean iguales. Se aprovecha que la cantidad de duales siempre será par.
    tabla_final_p2['igual2']=tabla_final_p2['igual1']

    for i in range(int(len(tabla_final_p2.index)/2)):  
        if tabla_final_p2.index[i][:tabla_final_p2.index[i].find('-')]==tabla_final_p2.index[
                                    i+int(len(tabla_final_p2.index)/2)][:tabla_final_p2.index[
                                    i+int(len(tabla_final_p2.index)/2)].find('-')]:
            tabla_final_p2.iloc[i+int(len(tabla_final_p2.index)/2),-1]=tabla_final_p2.iloc[i,-2]

    # Quinto: Se toman máscaras desde cero hasta la mitad de la tabla de bonos duales.
    # Esto permite obtener una tabla con dos bonos duales que son lo mismo pero están 
    # valorados con CER en un caso y con DL en el otro. De esta tabla se elige el bono
    # DUAL con el mayor rendimiento, y con éste se crea la tabla de bonos duales definitiva.
    tabla_final_p3=[]
    tabla_final_p3=pd.DataFrame(tabla_final_p3)

    for i in range(int(len(tabla_final_p2.index)/2)):
        a=tabla_final_p2.loc[tabla_final_p2.igual2==i].sort_values(
                                                'RT_Anual_Esp',ascending=False).iloc[0,0:]
        tabla_final_p3=pd.concat([tabla_final_p3,a],axis=1)

    # Sexto: Se ordenan las tablas de bonos duales y no duales.
    tabla_final_p3=tabla_final_p3.T
    tabla_final_p3=tabla_final_p3.drop(['DUAL','igual1','igual2'],axis=1)
    tabla_final_p1=tabla_final_p1.drop('DUAL',axis=1)

    # Séptimo: Se crea la tabla definitiva, uniendo las tablas de bonos duales definitiva 
    # con la tabla de bonos que no son duales. 
    tabla_definitiva=pd.concat([tabla_final_p1,tabla_final_p3],axis=0).sort_values(
                                            'RT_Anual_Esp',ascending=False)

    return tabla_definitiva
    
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# BUSCAR INFORMACION SOBRE LA FUNCION ENUMERATE, PASAR LA DESCRIPCION EN EL 
# DOCUMENTO DE PROGRAMACION + SUMAR LA EXPLICACION SOBRE COMO COLOCAR LAS ETIQUE
# TAS + CÓMO OBTENER LOS PARÁMETROS DE UNA REGRESION Y CÓMO GRAFICAR SU RECTA.










