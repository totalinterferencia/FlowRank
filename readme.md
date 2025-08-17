# 📊 FlowRank

FlowRank es un **screener de criptomonedas** que utiliza la relación **volumen/marketcap** (`rel_volume = volumen_24h / marketcap`) para detectar tokens con alta rotación de capital.  
Se centra exclusivamente en **pares USDT de Binance**, excluye automáticamente las stablecoins y muestra en consola el **TOP 20** de activos con mayor actividad relativa.

---

## 🚀 Características

- Filtra **solo pares USDT** listados en Binance.  
- Excluye **stablecoins** usando el flag del feed y una heurística de precio ≈ 1.  
- Calcula la métrica principal:  
  ```
  rel_volume = volume_24h / marketcap
  ```
- Muestra en consola el **TOP 20** tokens con mayor rotación de capital.  
- No genera CSV ni archivos externos: todo se imprime en pantalla.  

---

## 📥 Instalación

Clonar el repositorio y entrar a la carpeta:

```bash
git clone https://github.com/tuusuario/flowrank.git
cd flowrank
```

Instalar dependencias necesarias:

```bash
pip install requests pandas numpy
```

---

## ▶️ Uso

Ejecutar directamente el script:

```bash
python flowrank.py
```

### Ejemplo de salida

```
=== FlowRank — Binance (USDT) — TOP 20 por rel_volume (excluyendo stablecoins) ===

symbol   name        price   change_24h   volume_24h     market_cap   rel_volume
SOL      Solana      180.5       3.2%   1.23e+09      7.50e+10      0.016
DOGE     Dogecoin      0.15       4.1%   8.95e+08      2.05e+10      0.044
...
```

---

## 📊 ¿Qué es `rel_volume`?

Es la relación entre el **volumen negociado en 24h** y la **capitalización de mercado**:

- **Bajo:** poca rotación, mercado estable.  
- **Medio:** actividad saludable.  
- **Alto:** flujo inusual de capital, posible señal de interés especulativo o institucional.  

Este indicador es útil porque permite comparar activos grandes y pequeños bajo la misma escala, eliminando el sesgo del volumen absoluto.

---

## 🌐 Proyecto

- Sitio web: [totalinterferencia.com](https://totalinterferencia.com)  
- Comunidad en Telegram: [t.me/totalinterferencia_comunidad](https://t.me/totalinterferencia_comunidad)  


---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!  
Podés abrir un **issue** o un **pull request** en GitHub para proponer mejoras, reportar bugs o sumar ideas.

---

## ⚠️ Disclaimer

FlowRank es una herramienta educativa y experimental.  
No constituye asesoramiento financiero ni recomendación de inversión.  
Cada usuario es responsable de sus decisiones en el mercado.

