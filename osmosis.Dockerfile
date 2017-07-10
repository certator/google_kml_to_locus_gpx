FROM java:8

RUN mkdir -p /opt/osmosis /opt/maven
WORKDIR /opt/osmosis
ARG OSMOSIS_VERSION
RUN wget "http://bretth.dev.openstreetmap.org/osmosis-build/osmosis-${OSMOSIS_VERSION}.tgz" -O osmosis.tgz
RUN tar xvf osmosis.tgz
RUN rm osmosis.tgz
RUN chmod a+x bin/osmosis

RUN mkdir -p /opt/gradle
WORKDIR /opt/gradle
ARG GRADLE_DIR="gradle-3.3"
ARG GRADLE_URL="https://services.gradle.org/distributions/gradle-3.3-bin.zip"
RUN wget ${GRADLE_URL} -O /tmp/gradle-bin.zip
RUN unzip /tmp/gradle-bin.zip
#ENV PATH="/opt/gradle/gradle-4.0.1/bin:${PATH}"
ENV PATH="/opt/gradle/${GRADLE_DIR}/bin:${PATH}"

RUN mkdir -p /opt/mapsforge
WORKDIR /opt/mapsforge
COPY mapsforge.build.gradle /opt/mapsforge/build.gradle
RUN gradle copyToLib
WORKDIR /opt/osmosis/lib/default
RUN cp /opt/mapsforge/build/output/libs/* ./

WORKDIR /opt/osmosis
ENV JAVA_OPTS="-Xmx6G -Xms1G -d64 -server"
ENV JAVACMD_OPTIONS="${JAVA_OPTS}"

#ENV JDK_JAVA_OPTIONS="--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --permit-illegal-access"