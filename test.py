from rmbconvert import Traditional

if __name__ == "__main__":
    rmb = Traditional("伍佰叁拾玖万零贰拾壹元叁角伍分")
    number = rmb.to_number()
    print(number)
