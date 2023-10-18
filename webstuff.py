from flask import Flask, request
from decimal import Decimal

app = Flask(__name__)

@app.route("/")
def entry_point():
    return """
    <html data-theme="dark">
        <header>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
        </header>
        <body class="container-fluid">
                <form action="/tipout" method="post" id="form1">
                    <label >CC Tips: </label>
                    <input type="text" inputmode="numeric" name="cctips"><br>
                    <label >Cash Tips:</label>
                    <input type="text" inputmode ="numeric" name="cashtips"><br>
                    <label >Food Sales:</label>
                    <input type="text" inputmode="numeric" name="fsales"><br>
                    <label >Net Sales:</label>
                    <input type="text" inputmode="numeric" name="nsales"><br>
                    <label >Individual Bar Sales:</label>
                    <input type="text" inputmode="numeric" name="bsales">
                    <button type="submit" form="form1" >Calculate</button>
                </form>
        </body>
    </html>
    
    <style>
        :root {
        margin-top:-120px;
        --font-size: 30px;
        }
    </style>"""

@app.route("/tipout", methods = ['GET', 'POST'])
def ehello_world():
    food_tip_perc = Decimal('.02')
    net_tip_perc = Decimal('.03')
    bar_tip_perc = Decimal('.05')

    sales_dict = request.form

    def bar_list(bar_sales):
        res = []
        table = bar_sales.maketrans(" ,+", "   ")
        bar_sales = bar_sales.translate(table)
        for num in bar_sales.split():
            res.append(float(num))
        return res

    def bar_add(bararr: list[float]):
        result = 0.0
        for num in bararr:
          result += num
        return Decimal(result)
    
    bar_sales_total = Decimal(0)
    if sales_dict['bsales']:
        bar_sales_total = round(Decimal(bar_add(bar_list(sales_dict['bsales']))))

    food_tip = Decimal(0)
    net_tip = Decimal(0)
    bar_tip = Decimal(0)
    cctip = Decimal(0)
    cashtip = Decimal(0)
    net_sales = Decimal(0)
    tip_avg = Decimal(0)
    food_sales = Decimal(0)

    if sales_dict['fsales']:
        food_sales = sales_dict['fsales']
        food_tip = round(Decimal(sales_dict['fsales']) * food_tip_perc, 2)
    if sales_dict['nsales']:
        net_tip = round(Decimal(sales_dict['nsales']) * net_tip_perc, 2)
        net_sales = Decimal(sales_dict['nsales'])
    bar_tip = round(bar_sales_total * bar_tip_perc, 2)
    total_tipped = round(food_tip + net_tip + bar_tip, 2)
    if sales_dict['cctips']:
        cctip = Decimal(sales_dict['cctips'])
    if sales_dict['cashtips']:
        cashtip = Decimal(sales_dict['cashtips'])
    tips = Decimal(cctip) + Decimal(cashtip)
    take_home = round(tips - total_tipped, 2)
    def divide(x):
        if x > 0:
            return round(Decimal(x / tips * 100))
        else:
            return Decimal(0)
    percent_tipped_total = round(divide(total_tipped))
    percent_tipped_bar = round(divide(bar_tip))
    percent_tipped_food = round(divide(food_tip))
    percent_tipped_net = round(divide(net_tip))
    if net_sales > 0:
        tip_avg = round((tips / net_sales) * 100)
    

    str = f"""
        <html data-theme="dark">
            <header>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
            </header>
            <body>
                <p style="font-size:40px"> 5% Bar Sales: ${bar_tip} ({percent_tipped_bar}%)<br>
                <p style="font-size:40px"> Net Sales: ${net_sales}<br>
                <p style="font-size:40px"> Food Sales: ${food_sales}<br>
                <p style="font-size:40px"> Bar Sales: ${bar_sales_total}<br>
                <p style="font-size:40px"> CC Tips: ${cctip}<br>
                <p style="font-size:40px"> Cash Tips: ${cashtip}<br>
                <p style="font-size:40px"> 2% Food Sales: ${food_tip} ({percent_tipped_food}%)<br> 
                <p style="font-size:40px"> 3% Net Sales: ${net_tip} ({percent_tipped_net}%)<br>
                <p style="font-size:40px"> Total Tipped Out: ${total_tipped} ({percent_tipped_total}%)<br>
                <p style="font-size:40px"> Take Home Tips: ${take_home}</p><br><br>
                <p style="font-size:40px"> TIPS BEFORE TIPOUT: ${tips} ({tip_avg}% Combined Tip Avg)<br>
                
                <form action="/" method="get">
                    <button type="submit" >Return</button>
                </form>
            </body>
        </html>"""
    
    return str