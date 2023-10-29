from datetime import datetime



def convert_time_to_am_pm(time_str):
    try:
        # Parse the input time string
        input_time = datetime.strptime(time_str, "%H:%M")

        # Check if the time is exactly at midnight (00:00)
        if input_time.time() == datetime.min.time():
            output_time = "00:00am"
        elif input_time.time() == datetime.max.time():
            output_time = "12:00pm"
        else:
            # Format the time in 12-hour format with AM/PM
            formatted_time = input_time.strftime("%I:%M%p").lstrip("0").replace(" 0", " ")
            # If the formatted time starts with "0", replace it with "0" instead of "00"
            if formatted_time.startswith("0"):
                formatted_time = "0" + formatted_time[1:]

            if time_str.split(":")[0] == "00":
                formatted_time = "00:"+formatted_time.split(":")[1]

            output_time = formatted_time

            print(output_time, time_str, " : pl")

        return output_time
    except ValueError:
        return "Invalid time format"




def prepare_trade_graph(trades):
    profit_x_axis = []
    profit_line = []

    loss_x_axis = []
    loss_line = []

    loss_count = 1
    profit_count = 1

    for trade in trades:
        if loss_count and profit_count > 11:
            break # only most recent 10 is enough for profit and loss

        trade_time = str(trade.closing_time.time())
        time = trade_time.split(":")
        refactored_time = time[0]+":"+time[1]
        refined = convert_time_to_am_pm(refactored_time)

        entry= round(trade.amount_traded/100, 2)
        closing= round(trade.closing_amount/100, 2)

        margin = closing-entry

        trade_close_date = str(trade.closing_time.date())

        if margin < 0 :
            if loss_count > 11:
                continue # only most recent 10 is enough so skip loop

            # add to loss stroke
            loss_line.append(abs(margin))
            loss_x_axis.append(refined)
            loss_count += 1
        else:
            if profit_count > 11:
                continue # only most recent 10 is enough so skip loop

            profit_line.append(margin)
            profit_x_axis.append(refined)
            
            profit_count += 1

    profit_x_axis.reverse()
    profit_line.reverse()

    loss_x_axis.reverse()
    loss_line.reverse()


    return profit_x_axis, loss_x_axis, profit_line, loss_line 
