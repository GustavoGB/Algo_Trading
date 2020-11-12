class ARIMATick(Strategy):

    def __init__(self):
        self.prices = []
        self.position = 0
        self.threshold = 100

    def push(self, event):
        if event.type == Event.TRADE:
            price = event.price
            self.prices.append(price)
            orders = []
            if len(self.prices) > self.threshold:
                model = sm.tsa.ARIMA(self.prices, (1,1,1)).fit()
                # Previsão do próximo ponto
                forecast_list = []
                for i in range(1,10):
                    forecast_list.append(model.forecast(steps=i)[0][0])
                forecast_median = np.median(forecast_list)
                
                # Se o preço previsto for maior que o preço atual, compra, senão vende.
                decision = 0
                if forecast_median > price:
                    decision = 1
                elif forecast_median < price:
                    decision = -1    
                if decision == -1 and self.position != 1:
                    if self.position == 0:
                        orders.append(Order(event.instrument, 100, 0))
                    else:
                        orders.append(Order(event.instrument, 200, 0))
                elif decision == 0 and self.position != 0:
                    if self.position == 1:
                        orders.append(Order(event.instrument, 100, 0))
                    else:
                        orders.append(Order(event.instrument, -100, 0))
                elif decision == 1 and self.position != -1:
                    if self.position == 0:
                        orders.append(Order(event.instrument, -100, 0))
                    else:
                        orders.append(Order(event.instrument, -200, 0))
                self.position = decision

            return orders
        return []