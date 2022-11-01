# A complete guide for writing Dockerfile

- [A complete guide for writing Dockerfile](#a-complete-guide-for-writing-dockerfile)
  - [0. Ôn luyện](#0-ôn-luyện)
    - [0.1. Giới thiệu về Docker image và Dockerfile](#01-giới-thiệu-về-docker-image-và-dockerfile)
    - [0.2. Giới thiệu về build context](#02-giới-thiệu-về-build-context)
  - [1. Best practices to reduce image size and speed up build time](#1-best-practices-to-reduce-image-size-and-speed-up-build-time)
    - [1.1. Chọn đúng base image](#11-chọn-đúng-base-image)
    - [1.2. Loại bỏ file không cần thiết](#12-loại-bỏ-file-không-cần-thiết)
    - [1.3. Sử dụng multi-stage builds](#13-sử-dụng-multi-stage-builds)
    - [1.3. Loại bỏ/không cài đặt các gói không cần thiết và caching](#13-loại-bỏkhông-cài-đặt-các-gói-không-cần-thiết-và-caching)
    - [1.4. Tách các ứng dụng](#14-tách-các-ứng-dụng)
    - [1.5. Giảm thiểu tối đa số lượng layers](#15-giảm-thiểu-tối-đa-số-lượng-layers)
    - [1.6. Tận dụng build cache](#16-tận-dụng-build-cache)
  - [2. Best practices for maintainability](#2-best-practices-for-maintainability)
    - [2.1. Luôn sử dụng official image nếu có thể](#21-luôn-sử-dụng-official-image-nếu-có-thể)
    - [2.2. Sử dụng tag cụ thể](#22-sử-dụng-tag-cụ-thể)
  - [3. Best practices for container security](#3-best-practices-for-container-security)
    - [3.1. Sử dụng build-args thay vì environment](#31-sử-dụng-build-args-thay-vì-environment)
    - [3.2. Tránh cấp các đặc quyền không cần thiết](#32-tránh-cấp-các-đặc-quyền-không-cần-thiết)
      - [3.2.1. Rootless containers](#321-rootless-containers)
      - [3.2.2. Các file thực thi thuộc sở hữu của root và không cấp quyền sửa đổi](#322-các-file-thực-thi-thuộc-sở-hữu-của-root-và-không-cấp-quyền-sửa-đổi)
    - [3.3. Giảm thiểu attack surface](#33-giảm-thiểu-attack-surface)
      - [3.3.1. Multi-stage builds](#331-multi-stage-builds)
      - [3.3.2. Sử dụng trusted base images](#332-sử-dụng-trusted-base-images)
      - [3.3.3. Thường xuyên cập nhật images](#333-thường-xuyên-cập-nhật-images)
    - [3.4. Ngăn chặn rò rỉ dữ liệu mật](#34-ngăn-chặn-rò-rỉ-dữ-liệu-mật)
      - [3.4.1. Credentials và confidentiality](#341-credentials-và-confidentiality)
      - [3.4.2. ADD, COPY](#342-add-copy)

Source:

- <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>
- <https://sysdig.com/blog/dockerfile-best-practices/>
- <https://www.docker.com/blog/intro-guide-to-dockerfile-best-practices/>
- <https://gist.github.com/StevenACoffman/41fee08e8782b411a4a26b9700ad7af5>

## 0. Ôn luyện

Trước khi bắt đầu với những quy chuẩn, người đọc cần nắm được kiến thức tổng quát về Docker build.

### 0.1. Giới thiệu về Docker image và Dockerfile

- Dockerfile là file dạng text bao gồm các dòng đặc tả về Docker image, tuân theo định dạng [Dockerfile](https://docs.docker.com/engine/reference/builder/).
- Docker thực hiện tự động build images bằng cách đọc các đặc tả `Dockerfile`.
- Docker image được cấu thành bởi nhiều *read-only layers* (image layers), mỗi layer tương ứng mới một dòng đặc tả trong Dockerfile. Layer được xếp chồng lên nhau dạng stack, mỗi layer chứa các thay đổi so với layer trước nó.
- Ví dụ:

```Dockerfile
FROM ubuntu                  # This base image is already composed of X layers (4 at the time of writing)
MAINTAINER Florian Lopes     # One layer
RUN mkdir -p /some/dir       # One layer
RUN apt-get install -y curl  # One layer
```

![](https://www.codeproject.com/KB/Articles/1133826/Docker-layers.png)

- Khi chạy một image thành container, bản chất là thêm một *read-write layer* (container layer) ở trên các image layers. Mọi thay đổi ở container (ghi file mới, thay đổi file, xóa file,...) đều được ghi vào container layer.

### 0.2. Giới thiệu về build context

- Thư mục chạy `docker build` command gọi là *build context*. Mặc định, đây là thư mực chứa Dockerfile, tuy nhiên có thể chỉ định đường dẫn của Dockerfile bằng option `-f`.
- Build context bao gồm tất cả nội dung của các file và thư mục con của thư mục hiện tại, được gửi về Docker daemon trong quá trình build.
- Docker hỗ trợ build images bằng cách piping Dockerfile thông qua stdin. Khi đó, nội dung Dockerfile được đọc trực tiếp mà không cần lưu lại dưới dạng file trong ổ đĩa. Tuy nhiên, trong giới hạn tài liệu này, chúng ta chỉ lấy ví dụ Dockerfile dạng file bình thường.

```shell
echo -e 'FROM busybox\nRUN echo "hello world"' | docker build -

docker build -<<EOF
FROM busybox
RUN echo "hello world"
EOF
```

## 1. Best practices to reduce image size and speed up build time

Mọi practices viết Dockerfile đều để đạt được mục tiêu cuối cùng là tối ưu hóa quá trình build image. Điều đó có thể đạt được bằng cách:

- Giảm kích thước của image.
- Tăng tốc độ build image.

### 1.1. Chọn đúng base image

- Lựa chọn base image phù hợp là bước đầu tiên trong quá trình tối ưu hóa build phase. Việc lựa chọn base image phụ thuộc vào nhiều điều kiện như loại ứng dụng bạn mong muốn chạy trên container.
- Thông thường các bạn nên lựa chọn image do cộng Docker build sẵn làm base image. Các base image này đã được tối ưu nhất. Ví dụ, ứng dụng yêu cầu chạy ứng dụng Nginx, thay vì tự build image từ base ubuntu, sau đó cài đặt nginx và các gói liên quan, bạn có thể sử dụng image [nginx](https://hub.docker.com/_/nginx).
- Nếu bắt buộc phải sử dụng một base image tổng quan, có 2 lựa chọn: [alpine](https://hub.docker.com/_/alpine) và [debian-slim](https://hub.docker.com/_/debian).
- Alpine Linux là một distro linux dựa trên musl và BusyBox, được phát triển chú trọng về đơn giản, bảo mật và hiệu quả tài nguyên. Tuy nhiên Alpine có một số hạn chế:
  - Alpine sử dụng musl libc, trong khi debian sử dụng GNU libc, do đó tương thích là một vấn đề cần lưu ý khi sử dụng Alpine.
  - Cộng đồng phát triển của alpine không lớn như debian nên các phần mềm trên alpine có thể bị cập nhật phiên bản chậm hơn hoặc thiếu một số phần mềm.
- Do vậy, **base image alpine thường được sử dụng với các dự án microservice, khi có số lượng service lớn**, nhằm tối ưu dung lượng. Còn đối với **những dự án khi số lượng service nhỏ (<10) thì xây dựng Dockerfile dựa trên debian-slim** vẫn dễ dàng và an toàn hơn.

### 1.2. Loại bỏ file không cần thiết

- Không phải mọi file trong file đều cần thiết cho quá trình build image. Ví dụ, thư mục `.git` rõ ràng là không cần thiết nếu như trong quá trình build không dùng dến tính năng version control.
- Do vậy, bạn hoàn toàn có thể bỏ quả các file này bằng cách sử dụng [.dockerignore file](https://docs.docker.com/engine/reference/builder/#dockerignore-file).
- Ngoài ra, có thể chủ động chỉ định file sử dụng trong đặc tả `COPY`, thay vì `COPY .` (copy all).

### 1.3. Sử dụng multi-stage builds

- Multi-stage builds là một tính năng mới được giới thiệu từ Docker v17.05. Multi-stage builds rất hữu ích khi bạn muốn tối ưu hóa Dockerfile mà vẫn giữ cho nó vừa dễ đọc, vừa dễ maintain.
- Chương trình thường chỉ cần 1 hoặc vài file thực thi và cấu hình. Để build các file thực thi đó, cần cài đặt môi trường, gói, module,... tuy nhiên, khi chạy chương trình lại không cần môi trường này. Với multi-stage builds, bạn có thể cô lập môi trường build trong một stage, môi trường chạy chương trình trong stage khác, nhờ vậy, kích thước image sẽ nhỏ hơn, nhưng không làm ảnh hưởng đến việc thực thi chương trình.
- Ngoài ra, khi sử dụng multi-stage builds, bạn cũng có thể giảm thiểu số lượng layers bằng cách dựa vào build cache - chi tiết sẽ được nói đến trong phần Tận dụng build cache phía dưới.
- Multi-stage builds thường được sử dụng với dự án sử dụng Golang, Java, React, Angular,... - các dự án có bước build. Ví dụ, Dockerfile cho ứng dụng Golang:

```Dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.16-alpine AS build

# Install tools required for project
# Run `docker build --no-cache .` to update dependencies
RUN apk add --no-cache git
RUN go get github.com/golang/dep/cmd/dep

# List project dependencies with Gopkg.toml and Gopkg.lock
# These layers are only re-built when Gopkg files are updated
COPY Gopkg.lock Gopkg.toml /go/src/project/
WORKDIR /go/src/project/
# Install library dependencies
RUN dep ensure -vendor-only

# Copy the entire project and build it
# This layer is rebuilt when a file changes in the project directory
COPY . /go/src/project/
RUN go build -o /bin/project

# This results in a single layer image
FROM scratch
COPY --from=build /bin/project /bin/project
ENTRYPOINT ["/bin/project"]
CMD ["--help"]
```

- Bạn có thể tham khảo thêm [NodeJS application example](https://github.com/Coffee-WIP/coffeewip-website/blob/master/Dockerfile) và [Python Django multi-stage build](https://github.com/Coffee-WIP/coffeewip-website/blob/master/Dockerfile).

### 1.3. Loại bỏ/không cài đặt các gói không cần thiết và caching

- Đây có vẻ là một điều đương nhiên, nhưng không phải ai cũng thực sự tuân thủ. Người dùng thường có xu hướng cài đặt mọi thứ có thể phải dùng vào trong Dockerfile: text editor, công cụ troubleshoot, debug... Điều này làm tăng kích thước của image lên đáng kể.

![](https://www.docker.com/wp-content/uploads/2019/07/a1b36f64-1a30-45bf-8fcd-4f88437c189e.jpg)

- Bên cạnh đó, package manager cache cũng cần được xóa. Cache là bộ nhớ tạm lưu trữ tạm thời được sử dụng để tăng tốc độ truy cập dữ liệu thường xuyên. Tuy nhiên, trong Docker image, cache không có nhiều ý nghĩa.

![](https://www.docker.com/wp-content/uploads/2019/07/363961a4-005e-46fc-963b-f7b690be12ef.jpg)

### 1.4. Tách các ứng dụng

- Một lỗi khác hay mắc phải đó chính là cố gắng chạy nhiều ứng dụng trong cùng một container, giống như một máy ảo. Ví dụ, cài đặt `supervisorctl` trong image để quản lý một vài ứng dụng khác.
- Mỗi container chỉ nên thực thi một chương trình duy nhất. Chia nhỏ các tác vụ và chạy các container khác nhau cho mỗi tác vụ, như vậy kích thước của image sẽ nhỏ hơn, build cũng nhanh chóng hơn. Chúng ta có thể thực hiện chạy build nhiều image đồng thời, nếu các image có chung phần base, cache sẽ được sử dụng.
- Mở rộng hơn nữa, trong quá trình chạy container, chia nhỏ các tác vụ thành các container cũng giúp việc mở rộng theo chiều ngang (scale out/in) dễ dàng hơn.

### 1.5. Giảm thiểu tối đa số lượng layers

- Như đã nói ở phần 0, Docker image được cấu thành từ nhiều layers. Các layer không phải là *free*. Chúng chiếm dụng không gian và khi layer xếp chồng lên nhau ngày càng nhiều thì kích thước image cuối cùng của bạn cũng tăng lên. Nguyên nhân là do hệ thống sẽ lưu giữ tất cả các thay đổi giữa các đặc tả Dockerfile khác nhau. Do vậy. giảm số lượng layer là điều cần làm khi muốn giảm kích thước images.
- Các đặc tả `RUN`, `COPY`, `ADD` tạo ra layer vì chúng thay đổi file system. Các đặc tả khác tạo ra các layer tạm, không làm ảnh hưởng đến kích thước của image.
  - Lấy ví dụ một Dockerfile đơn giản như sau:
  
  ```Dockerfile
  FROM ubuntu:18.04
  
  WORKDIR /var/www
  
  RUN apt-get update
  RUN apt-get -y install curl
  RUN apt-get -y install vim
  ```

  - Thực hiện build image và kiểm tra các layers được tạo ra:

  ```shell
  docker history ubuntu:example  
  IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
  3254f0ec9c48        8 minutes ago       /bin/sh -c apt-get -y install vim               54.8MB             
  dac7e4ba12f9        8 minutes ago       /bin/sh -c apt-get -y install curl              14.3MB             
  be0ed9278c8f        2 hours ago         /bin/sh -c apt-get update                       34.1MB             
  a6494da55123        2 hours ago         /bin/sh -c #(nop) WORKDIR /var/www              0B                 
  56def654ec22        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B                 
  <missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B                 
  <missing>           2 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B                 
  <missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B               
  <missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:4974bb5483c392fb5…   63.2MB
  ```

  - Có thể thấy image có 3 layers riêng biệt cho update và install. Thay vì thế, gộp các layers lại và xóa cache sau khi cài đặt:

  ```Dockerfile
  FROM ubuntu:18.04
  
  WORKDIR /var/www

  RUN apt-get update && \
      apt-get install --no-install-recommends \
      curl vim -y && \
      apt-get autoremove -y && \
      apt-get autoclean -y && \
      rm -rf /var/lib/apt/lists/*
  ```

- Nếu có thể, hãy sử dụng multi-stage builds.

### 1.6. Tận dụng build cache

- Khi build image, Docker thực thi từng dòng đặc tả trong Dockerfile, theo thứ tự xuất hiện. Tuy nhiên, thay vì tạo ngay một image mới, Docker kiểm tra xem có image nào có thể dùng được trong cache. Quá trình được thực hiện như sau:
  - Kiểm tra parent image, nếu image này đã thỏa mãn, ở trong cache, tiếp tục kiểm tra các child images xem có image nào trong đó thực thi đặc tả đang cần tìm cache. Nếu không có, cache tính là invalidated, Docker tạo image mới như bình thường.
  - Đối với đặc tả `ADD` và `COPY`, nội dung của file(s) được lấy ra, và dùng để tính toán ra một checksum tương ứng. Trong quá trình cache lookup, Docker so sánh checksum này với checksum của image trong cache. Nếu có bất kỳ thay đổi nào trong file(s), checksum thay đổi, đồng nghĩa với việc cache bị invalidated.
  - Ngược lại, đối với các đặc tả khác, chỉ command string được sử dụng để so sánh.
- Từ đó, chúng ta sẽ có một số cách Sau đây để tận dụng build cache.
- Sắp xếp để tận dụng được cache: lấy ví dụ như sau, thay vì `COPY` files trước khi thực hiện update và install, hãy chuyển `COPY` ra sau. Bởi vì files thường sẽ bị thay đổi, do vậy cache tính là invalidated do vậy tính từ C`OPY, mỗi đặc tả đều cần tạo image mới. Trong khi đó, nếu thực hiện `COPY` ra sau, bạn có thể tận dụng image đã được update và install ở trong cache.

![](https://www.docker.com/wp-content/uploads/2019/07/ef41db8f-fe5e-4a78-940a-6a929db7929d-1.jpg)

- Thay vì copy tất cả files trong build context vào trong image, hãy chỉ định rõ file cần copy đặc tả `COPY`. Như vậy, loại bỏ các file không cần thiết mà thường xuyên thay đổi, làm thay đổi checksum. Bạn có thể để file thường thay đổi (dĩ nhiên là cần thiết cho quá trình build) ở phía sau để tận dụng tối đa cache.

![](https://www.docker.com/wp-content/uploads/2019/07/0c1d0c4e-406c-468c-b6ba-b71ac68b9c84.jpg)

- Tận dụng tối đa các cachable unit như RUN update và install.

## 2. Best practices for maintainability

### 2.1. Luôn sử dụng official image nếu có thể

- Như đã nói phía trên, official image là những image được tối ưu hóa. Hãy sử dụng các image này làm base image nếu có thể.

### 2.2. Sử dụng tag cụ thể

- Người dùng thường sử dụng tag latest trong Dockerfile. Latest chỉ mang tính chất tương đối ở thời điểm build, ví dụ, khi build image openjdk 7 là latest, nhưng thời gian sau, openjdk 11 mới là latest, ứng dụng có thể không còn tương thích. Người dùng sẽ không biết đâu version của base image, gây khó khăn cho việc troubleshooting nếu có lỗi xảy ra.
- Thay vì thế, hãy dùng tag cụ thể trong Dockerfile.

![](https://www.docker.com/wp-content/uploads/2019/07/9d991da9-bdb9-4108-8b36-296a5a3772aa.jpg)

## 3. Best practices for container security

### 3.1. Sử dụng build-args thay vì environment

- Trong môi trường kết nối bị kiểm soát qua proxy, người dùng hay thêm http/https proxy vào đặc tả ENV trong Dockerfile.

```Dockerfile
FROM ubuntu:22.04

ENV http_proxy http://proxy
ENV https_proxy https://proxy
```

- Đương nhiên, build hoạt động bình thường. Tuy nhiên, về sau khi sử dụng image, nếu `docker history`, bạn vẫn có thể lấy được thông tin proxy của công ty. Ngoài ra, http/https proxy trong môi trường có thể làm sai lệch hoạt động của ứng dụng.
- Vì vậy, không bao giờ expose ENV dạng proxy trong Dockerfile. Thay vào đó, sử dụng [`--build-args`](https://docs.docker.com/engine/reference/commandline/build/).

### 3.2. Tránh cấp các đặc quyền không cần thiết

#### 3.2.1. Rootless containers

- Theo một [báo cáo của Sysdig](https://sysdig.com/blog/sysdig-2021-container-security-usage-report/), có đến 58% images đang dùng entrypoint chạy bằng **root** (**UID 0**).
- Để chạy rootless container, cần lưu ý:
  - Đảm bảo user chỉ định tại USER tồn tại.
  - Cung cấp quyền thích hợp cho files tại nơi process thực hiện đọc/ghi. Ví dụ, process thực hiện ghi log vào file, phải có quyền đọc ghi.

  ```Dockerfile
  FROM alpine:3.12
  # Create user and set ownership and permissions as required
  RUN adduser -D myuser && chown -R myuser /myapp-data
  # ... copy application files
  USER myuser
  ENTRYPOINT ["/myapp"]
  ```

- Container có thể chạy dùng root user, sau đó sử dụng [gosu](https://github.com/tianon/gosu) hoặc  [su-exec](https://github.com/ncopa/su-exec) để chuyển sang user thường.

#### 3.2.2. Các file thực thi thuộc sở hữu của root và không cấp quyền sửa đổi

- Tất cả các file thực thi trong container phải để owner là root, kể cả các file được thực thi bởi non-root user và không thể sửa đổi.
- Điều này không cho phép user chỉnh sửa các file thực thi/script, từ đó dẫn đến các tấn công khác.
- Tránh thay đổi quyền như ví dụ sau, `app` user **không cần ownership**, chỉ cần quyền execution.

```Dockerfile
...
WORKDIR $APP_HOME
COPY --chown=app:app app-files/ /app
USER app
ENTRYPOINT /app/my-app-entrypoint.sh
```

### 3.3. Giảm thiểu attack surface

- Loại bỏ các gói không cần thiết hoặc hạn chế expose ports sẽ giảm thiểu attack surface. Càng nhiều thành phần trong container, đồng nghĩa với việc càng nhiều nguy cơ bị tấn công.

#### 3.3.1. Multi-stage builds

- Phần này đã nói phía trên nên không trình bày lại.

#### 3.3.2. Sử dụng trusted base images

- Luôn sử dụng official images ở trused repositories, đây là những image đã được tối ưu hóa về kích thước cũng như cập nhật thường xuyên các bản vá bảo mật.

#### 3.3.3. Thường xuyên cập nhật images

- Thường xuyên cập nhật images để cập nhật các bản vá fix lỗi bảo mật.
- Do vậy, bạn cần:
  - Sử dụng phiên bản stable hoặc long-term support (LTS).
  - Cập nhật base image lên phiên bản mới trước khi EOL: Nếu bạn sử dụng ubuntu:18.04 (đã EOL) làm base image tại thời điểm 2022, cập nhật lên phiên bản ubuntu còn được hỗ trợ.
  - Định kỳ build lại image để cập nhật phiên bản mới nhất của các gói.

### 3.4. Ngăn chặn rò rỉ dữ liệu mật

#### 3.4.1. Credentials và confidentiality

- Không bao giờ để secret hoặc credentials vào Dockerfile! (Environment variables, Args, Hard coded trong CMD).
- Lưu ý, kiểm tra các files copy vào trong container, tốt nhất nên chỉ định rõ file được COPY/ADD hoặc sử dụng `.dockerignore`.

#### 3.4.2. ADD, COPY

- `ADD` và `COPY` đều cho phép copy local files vào trong Docker image. Bên cạnh đó, `ADD` còn nhận đầu vào là remote URL hoặc file nén.
- Luôn sử dụng `COPY` thay vì `ADD` để tránh các vấn đề bảo mật tiềm ẩn:
  - `ADD` cho phép download file vào trong Docker image bằng remote URL, có thể xảy ra khả năng tấn công man-in-the-middle: thay đổi nội dung file được download về. Bên cạnh đó, nguồn gốc và tính xác thực remote URL cũng phải được kiểm tra.
  - Nếu dùng đầu vào là file nén, `ADD` tự động giải nén file này, vẫn có khả năng xảy ra tấn công sử dụng file nén (zip bombs, [zip slip vulnerabilities](https://snyk.io/research/zip-slip-vulnerability?utm_source=dzone&utm_medium=content&utm_campaign=content_promo&utm_content=cs_docker_security_10)).
