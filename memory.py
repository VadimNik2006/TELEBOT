# from difflib import SequenceMatcher


# @route.message(Keyword.wait_film)
# async def film_info(message: types.Message, state: FSMContext):
# prev_movies = (await state.get_data())['similar_list']
    # for_check = [re.sub(r'(\s+[^\w\s]\s+|[^\w\s]\s+|[^\w\s])', ' ', val.lower()) for val in prev_movies]
    #
    # print(f"for_check: {for_check}")
    #
    # user_message = re.sub(r'(\s+[^\w\s]\s+|[^\w\s]\s+|[^\w\s])', ' ', message.text.lower())
    # print(f"user_message: {user_message}")
    #
    # def message_index(user_message: str):
    #     for ind, el in enumerate(for_check):
    #         ind: int
    #         el: str
    #         similarity = SequenceMatcher(None, el, user_message).ratio()
    #         if (len(user_message) > 10 and similarity > 0.9) or (len(user_message) <= 10 and similarity >= 0.8):
    #             digit = [i for i in user_message.split() if i.isdigit()]
    #             if digit:
    #                 start_user_message_len, start_el_len = len(user_message), len(el)
    #                 b = user_message.replace(f" {digit[0]}", "")
    #                 c = el.replace(f" {digit[0]}", "")
    #                 end_user_message_len, end_el_len = len(b), len(c)
    #                 sim_b_c = SequenceMatcher(None, b, c).ratio()
    #                 if (end_user_message_len - start_user_message_len) == (end_el_len - start_el_len):
    #                     if (len(b) > 10 and sim_b_c > 0.9) or (len(b) <= 10 and sim_b_c >= 0.8):
    #                         return ind
    #                 else:
    #                     continue
    #             return ind
    #
    # my_def = message_index(user_message=user_message)
    # print(f"mes_index: {my_def}")
    # if type(my_def) is int:
    #     print("in condition")
    #     movie_index = my_def
    #     api_control = api_controller.get_similar_film(prev_movies[movie_index])
    #     # print(api_control)
    #     store = list()
    #     # print()
    #     # print()
    #
        # for index, elem in enumerate(api_control):
        #     # print(elem["nameRu"])
        #     # print(for_check[movie_index])
        #     # print()
        #     if elem["nameRu"].lower() == prev_movies[movie_index].lower():
        #         store.append(index)
        #         store.append(elem)
        #         # print("IN STORE", store)
        # data = store[0]
    #     #         await state.update_data({"selected_movie": (index, elem)})
    #     # data = (await state.get_data())["selected_movie"][0]
    #     user_id = message.from_user.id
    #     film_id = api_control[data]["kinopoiskId"]
    #     history_db(user_id=user_id, film_id=film_id)
    #     # print(user_id, film_id)
    #     await send_photo_with_bot(message=message, film_id=film_id, user_id=user_id, data=data, api_control=api_control,
    #                               db_con=db_controller.favorite_datas_view(user_id=user_id, film_id=film_id))
    #     # await message.bot.send_photo(user_id,
    #     #                              api_control[data]['posterUrlPreview'],
    #     #                              caption=api_control[data]['nameRu'],
    #     #                              reply_markup=power_kb(is_search=True,
    #     #                                                    is_liked=db_controller.favorite_datas_view(user_id, film_id),
    #     #                                                    id=film_id))
    #     await state.set_state(state=None)
    # else:
    #     await message.answer("Пожалуйста, скопируйте текст и попробуйте еще раз!")
