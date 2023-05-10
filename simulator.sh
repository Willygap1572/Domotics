#Definimos variables
CMD="python3"
CONTROLLER="controller.py"
SENSOR="dummy_sensor.py"
SWITCH="dummy_switch.py"
RULE="rule.py"
HOST="localhost"
export DJANGO_SETTINGS_MODULE='practica3.settings'
echo "Iniciando simulación por favor NO haga Ctrl+C ya que mata los procesos a los 15 segundos"
echo "---------------------"
echo "Iniciando controlador..."
#iniciamos el controlador
$CMD $CONTROLLER --host $HOST &
sleep 2
echo "Iniciando sensor..."
#iniciamos el sensor
$CMD $SENSOR --host $HOST 1 &
echo "Iniciando switch..."
#iniciamos el switch
$CMD $SWITCH --host $HOST 1 &
#creamos la rule
echo "Creando regla..."
$CMD $RULE &

# Esperar 15 segundos
sleep 15
echo "Simulación terminada"
# Matar todos los procesos
pkill -f $CMD