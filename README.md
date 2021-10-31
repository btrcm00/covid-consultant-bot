# Introduction

TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project.

# Getting Started

TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:

1. Installation process
2. Software dependencies
3. Latest releases
4. API references

# Build and Test

- There are 4 main folder in Hume-Chatbot:

  - backend

  - frontend

- To run all APIs, follow these requirements and commands:

  - There are 2 requirements files in folder "backend", "frontend", need install all libraries dependencies by following command:

    - Trong backend

    > pip install -r requirements.txt

  - Trong frontend, cài các package cần thiết

    > npm install

  - Chạy lệnh này tại thư mục gốc để cài đường dẫn tuyệt đối, tức là mọi thứ đều được import từ backend, ví dụ: from backend...... import .....:

    > pip install -e .

  - These commands run all APIs for chatbot:

    - In folder "backend":

    > cd backend
    > python app.py

    - In folder "frontend":

    > cd frontend
    > npm start

- Flow hoạt động

  - Khi bệnh nhân nhắn ở frontend, message sẽ được send đến api/send-message của fastapi backend
  - Sau đó sẽ khởi tạo instance CovidChat bot và lấy reply trả về từ bot này.
  - mọi giá trị trả về của file catch_intent.py đề phải dạng json

  ```
  {
    '<mã code chỉ hành động của bot (ví dụ request_age,....)>'{
  	  'infor':{...}
  	  'symptom': {...}
    }
  }
  ```

  - Sau đó dựa vào json trả về sẽ truyền vào generate_reply_text.py để tạo response.
