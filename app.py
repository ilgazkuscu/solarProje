def create_epdk_image():
    voltaj = [
        2.685, 2.687, 2.688, 2.690, 2.691, 2.692, 2.690, 2.688,
        2.689, 2.690, 2.688, 2.687, 2.685, 2.688, 2.690, 2.691,
        2.692, 2.690, 2.689, 2.688, 2.687, 2.686, 2.685, 2.688,
        2.690, 2.691, 2.690, 2.688, 2.687, 2.686, 2.685
    ]

    baslangic = datetime.now() - timedelta(minutes=30*(len(voltaj)-1))
    zaman = [baslangic + timedelta(minutes=30*i) for i in range(len(voltaj))]

    df = pd.DataFrame({
        "Zaman": [z.strftime("%d %b %H:%M") for z in zaman],
        "Fiyat (TL/kWh)": voltaj
    })

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(zaman, voltaj, color='orange', marker='.', linestyle='-', linewidth=1, markersize=5)
    ax.plot(zaman[-1], voltaj[-1], 'ro', markersize=10, label='Şu an')

    ax.set_title("EPDK Anlık Veri (TL / kWh)", fontsize=14)
    ax.set_ylabel("Fiyat (TL / kWh)")
    ax.legend()
    ax.grid(True)

    formatter = mdates.DateFormatter('%#d %b\n%H:%M')
    ax.xaxis.set_major_formatter(formatter)
    plt.subplots_adjust(bottom=0.3)

    table_data = df.tail(5).values
    column_labels = df.columns

    table = plt.table(cellText=table_data,
                      colLabels=column_labels,
                      cellLoc='center',
                      loc='bottom',
                      bbox=[0, -0.35, 1, 0.25])

    table.auto_set_font_size(False)
    table.set_fontsize(10)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_bytes = buf.read()
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()
