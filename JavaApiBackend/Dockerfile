FROM maven:3-amazoncorretto-17 AS build

WORKDIR /app

COPY pom.xml .
RUN mvn -B -f pom.xml dependency:go-offline
COPY . .
RUN mvn package -Dmaven.test.skip
CMD ["java", "-jar", "/app/target/appsec-1.jar"]
