import random


class DialogManager:
    """
    A class to manage dialog logic and generate responses based on user input.

    Attributes:
        responses: A dictionary mapping keywords to lists of generic responses.
        pers_responses: A dictionary mapping user IDs to dictionaries,
            where each dictionary maps keywords to lists of personalized responses for that user.
    """

    def __init__(self) -> None:
        self.responses: dict[str, list[str]] = {
            "hello": [
                "Привет, незнакомец.",
                "Здравствуй, друг!",
                "Приветик!",
            ],
            "goodbye": [
                "До свидания! Надеюсь, увидимся в следующий раз.",
                "Пока! Хорошего дня!",
                "До встречи! Береги себя!",
                "Прощай!",
                "Увидимся! Буду ждать твоего возвращения!",
            ],
            "thank_you": [
                "Пожалуйста!",
                "Рад был помочь!",
                "Не за что! Всегда рад помочь!",
                "Обращайся!",
            ],
            "who": [
                "Никто.",
                "Это может быть кто угодно...",
                "Хм... Это же очевидно...",
                "Некто особенный..",
            ],
            "what": [
                "Ничего.",
                "Я не знаю, что это такое. Если бы я знал, что это такое, но я не знаю, что это такое...",
                "Хм... Это же очевидно...",
                "Нечто особенное..",
            ],
            "where": [
                "Нигде.",
                "Там, где нужно.",
                "Может быть везде.",
                "Где угодно.",
                "Где-то.. не здесь.",
                "В Тюмени.",
                "В Праге.",
                "Не скажу, секретная информация.",
            ],
            "to_where": [
                "Туда.",
                "Сюда.",
                "Куда глаза глядят.",
                "Куда угодно.",
                "Куда-то...",
                "В Тюмень.",
                "Куда угодно.",
                "Не скажу, секретная информация.",
            ],
            "from_where": [
                "Оттуда.",
                "Отсюда.",
                "Откуда-то.",
                "Откуда угодно.",
                "Из Тюмень.",
                "Не скажу, секретная информация.",
            ],
            "when": [
                "Никогда.",
                "Завтра.",
                "Вчера.",
                "Когда-нибудь.",
                "Никогда не знаешь.",
                "Время покажет.",
                "Как получится.",
                "Я не знаю, спроси меня через годик.",
            ],
            "why": [
                "Потому что так.",
                "Обстоятельства...",
                "Нет однозначного ответа.",
                "Почему бы и нет?.",
                "Потому что... Нет, правда, не знаю!",
                "Причина может быть разной...",
                "Ответ на этот вопрос непрост.",
                "Понадобится когда-нибудь.",
            ],
            "kakaha": [
                "Сам такой",
                "А вот щас обидно было",
                "В зеркало это скажи",
            ],
            "how_are_you": [
                "Я? Отлично! Спасибо.",
                "Да вот грущу, жду, пока Влад настроит нормальные диалоги.",
                "Спроси попозже, я щас плохо соображаю.",
                "Вроде ничего, а у тебя как?",
            ],
            "how": [
                "Как? Вот так! У тебя есть еще какие-нибудь вопросы?",
                "Сложный вопрос! Как-то так...",
                "Здесь много вариантов...",
            ],
            "doing": [
                "Сплю, не мешай",
                "Ем",
                "Общаюсь с тобой",
            ],
            "other": [
                "Понял.",
                "Интересно... наверно...",
                "Понятно, очень интересно...",
                "Понял. Что дальше?",
                "Понимаю. Что предпочитаешь делать дальше?",
            ],
        }
        self.pers_responses: dict[int, list[str]] = {
            # Влад
            405992480: {
                "hello": [
                    "Привет, Владоний!",
                    "Привет, Владон!",
                    "Привет, Влад!",
                ],
            },
            # Женя
            483545491: {
                "hello": [
                    "Привет, Евгоська!",
                    "Привет, Евгос!",
                    "Привет, Евгосий!",
                    "Привет, Женидзе!",
                    "Привет, Женёк!",
                    "Привет, Женя!",
                ],
                "goodbye": [
                    "Покеда, Евгос.",
                    "Пока, Женечка",
                    "До встречи, Женя! Береги себя!",
                    "Ещё увидимся, Евгосий",
                ],
                "thank_you": [
                    "Все для тебя, Женя.",
                    "Рад был помочь, Евгос!",
                    "Не за что, Женя",
                    "Ой да перестань хи-хи",
                ],
                "other": [
                    "Женя не бузи.",
                    "Интересно... наверно...",
                    "Женя, хватит меня ломать...",
                    "Понял, Евгосий. Что дальше?",
                    "Понимаю. Что предпочитаешь делать дальше, Женя?",
                    "Евгос.. может что попроще?",
                ],
            },
            # Антон
            1103630666: {
                "hello": [
                    "Привет, Антон!",
                    "Привет, Аптоп!",
                    "Привет, Антоний!",
                    "Привет, Аптопич!",
                    "Привет, Антонидзе!",
                    "Привет, Антонио!",
                ],
            },
        }

    def handle_response(self, text: str, user_id: int = None) -> str:
        """
        Method to handle user messages and generate responses.

        Args:
            text: The string of user's message.
            user_id: Integer ID of the specific user. None by default.

        Returns:
            str: The generated prompt.
        """
        processed: str = text.lower()

        # hello
        if any(
            kw in processed
            for kw in [
                "привет",
                "приветик",
                "здравствуй",
                "здарова",
                "добрый день",
                "доброе утро",
                "добрый вечер",
                "здравствуйте",
            ]
        ):
            return self.handle_hello(user_id)
        # goodbye
        elif any(kw in processed for kw in ["пока", "до свидания"]):
            return self.handle_goodbye(user_id)
        # thank_you
        elif any(
            kw in processed for kw in ["спасибо", "спасибочки", "спасиб", "благодарю"]
        ):
            return self.handle_thank_you(user_id)
        # who
        elif "кто" in processed:
            return self.handle_who(user_id)
        # where
        elif "что" in processed:
            return self.handle_what(user_id)
        # where
        elif "где" in processed:
            return self.handle_where(user_id)
        # to_where
        elif "куда" in processed:
            return self.handle_to_where(user_id)
        # from_where
        elif "откуда" in processed:
            return self.handle_from_where(user_id)
        # when
        elif "когда" in processed:
            return self.handle_when(user_id)
        # why
        elif any(kw in processed for kw in ["почему", "зачем"]):
            return self.handle_why(user_id)
        # kakaha
        elif "какаха" in processed:
            return self.handle_kakaha(user_id)
        # how are you
        elif any(kw in processed for kw in ["как делишки", "как дела"]):
            return self.handle_how_are_you(user_id)
        # how
        elif "как" in processed:
            return self.handle_how(user_id)
        # doing
        elif "делаешь" in processed:
            return self.handle_doing(user_id)
        # other
        else:
            return self.handle_other(user_id)

    def handle_hello(self, user_id: int = None) -> str:
        """
        Method to generate a "hello" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "hello" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["hello"])
        return random.choice(self.responses["hello"])

    def handle_goodbye(self, user_id: int = None) -> str:
        """
        Method to generate a "goodbye" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "goodbye" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["goodbye"])
        return random.choice(self.responses["goodbye"])

    def handle_thank_you(self, user_id: int = None) -> str:
        """
        Method to generate a "thank you" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "thank_you" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["thank_you"])
        return random.choice(self.responses["thank_you"])

    def handle_who(self, user_id: int = None) -> str:
        """
        Method to generate a "who" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "who" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["who"])
        return random.choice(self.responses["who"])

    def handle_what(self, user_id: int = None) -> str:
        """
        Method to generate a "what" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "what" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["what"])
        return random.choice(self.responses["what"])

    def handle_where(self, user_id: int = None) -> str:
        """
        Method to generate a "where" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "where" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["where"])
        return random.choice(self.responses["where"])

    def handle_to_where(self, user_id: int = None) -> str:
        """
        Method to generate a "to where" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "to_where" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["to_where"])
        return random.choice(self.responses["to_where"])

    def handle_from_where(self, user_id: int = None) -> str:
        """
        Method to generate a "from where" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "from_where" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["from_where"])
        return random.choice(self.responses["from_where"])

    def handle_when(self, user_id: int = None) -> str:
        """
        Method to generate a "when" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "when" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["when"])
        return random.choice(self.responses["when"])

    def handle_why(self, user_id: int = None) -> str:
        """
        Method to generate a "why" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "why" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["why"])
        return random.choice(self.responses["why"])

    def handle_kakaha(self, user_id: int = None) -> str:
        """
        Method to generate a "kakaha" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "kakaha" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["kakaha"])
        return random.choice(self.responses["kakaha"])

    def handle_how_are_you(self, user_id: int = None) -> str:
        """
        Method to generate a "how_are_you" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "how_are_you" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["how_are_you"])
        return random.choice(self.responses["how_are_you"])

    def handle_how(self, user_id: int = None) -> str:
        """
        Method to generate a "how" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "how" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["how"])
        return random.choice(self.responses["how"])

    def handle_doing(self, user_id: int = None) -> str:
        """
        Method to generate a "doing" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "doing" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["doing"])
        return random.choice(self.responses["doing"])

    def handle_other(self, user_id: int = None) -> str:
        """
        Method to generate a "other" prompt.

        Args:
            user_id: Integer ID of the specific user in case there is one. None by default.

        Returns:
            str: The generated prompt.
        """
        if (
            user_id is not None
            and user_id in self.pers_responses
            and "other" in self.pers_responses[user_id]
        ):
            return random.choice(self.pers_responses[user_id]["other"])
        return random.choice(self.responses["other"])
