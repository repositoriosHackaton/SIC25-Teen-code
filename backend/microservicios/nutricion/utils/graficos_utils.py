import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.http import HttpResponse
from matplotlib.ticker import MultipleLocator, FuncFormatter

def configurar_estilo():
    """Configura el estilo de los gráficos."""
    sns.set_style("darkgrid")
    sns.set_palette("bright")
    plt.rcParams.update({
        'axes.facecolor': 'black',
        'figure.facecolor': 'black',
        'savefig.facecolor': 'black',
        'text.color': 'white',
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'legend.facecolor': 'black'
    })

def formato_tiempo(ax):
    """Formatea el eje X para mostrar el tiempo en horas y minutos."""
    ax.xaxis.set_major_locator(MultipleLocator(120))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{int(x // 60)}h {int(x % 60)}m' if x >= 60 else f'{int(x)}m'))

def render_grafico(fig):
    """Renderiza un gráfico en una respuesta HTTP."""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='image/png')
    plt.close(fig)
    return response