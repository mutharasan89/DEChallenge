# Senior Data Enginer Tech Challenge

## Section 3: System Design 1

---



When a table is created, it is assigned an owner. The initial state is that only the owner (or a superuser) can do anything with the object. Based on the requirement provided to us, each team must be granted with specific privileges using DCL commands. Usually DCL commands are executed by admins.

- Logistics team should be provided with select and update commands privileges using below DCL command 
<br>`GRANT SELECT, UPDATE ON orders TO <logistics_user>;`


- Analytics team should be provided with select only (perform analysis but cannot perform update)  privilege using below DCL command
<br>`GRANT SELECT ON orders TO <analytics_user>;`
<br>`GRANT SELECT ON products TO <analytics_user>;`

- Sales team should be provided with select, update , delete, truncate commands privileges using below DCL command
<br>`GRANT SELECT, UPDATE, DELETE, TRUNCATE ON orders TO <sales_user>;`
<br>`GRANT SELECT, UPDATE, DELETE, TRUNCATE ON products TO <sales_user>;`

---

## Section 3: System Design 2

---
Solution is provided assuming, we are going to leverage on Azure cloud services. Kindly refer to Untitled Diagram.drawio for the data flow architecture.

### Real time data stream Processing
Images file from streaming sources are consumed by Apache Spark [Azure event hub] and AKS provides a managed environment for the Apache Spark jobs.

An application that uses Azure Cosmos DB for Apache Cassandra writes events to Cassandra. This database serves as a storage platform for events. AKS hosts the microservices that write to Cassandra.
The change feed feature of Azure Cosmos DB processes events in real time.

The data further used for real-time applications.

### On-demand data processing

Users are provided with <b>WebApp</b> which has API functionality to upload image file to Cassandra [Azure Cosmos DB]. 

- Scheduled applications run batch-oriented processing on events [image files] stored in Cassandra.
Code is already built by software engineers and data scientist to process the images using Cognitive AI solution. Such code and scripts are one of the scheduled applications.
- Batch-oriented applications write the enriched event information [result of processed image files] to PostgreSQL.
- Postgres SQL DB relational data store provides data to downstream applications that require enriched information.
- Downstream applications : 
  - Reporting applications and tools analyze the PostgreSQL database data. For example, Power BI connects to the database by using the Azure Database for PostgreSQL connector. This reporting service then displays rich visuals of the data.
  - Azure Cache for Redis provides an in-memory cache. In this solution, the cache contains data on critical events. An application stores data to the cache and retrieves data from the cache.
  - Websites and other applications use the cached data to improve response times. Sometimes data isn't available in the cache. In those cases, these applications use the cache-aside pattern or a similar strategy to retrieve data from Cassandra in Azure Cosmos DB.

### Components

- Azure Event Hub :
  - Event Hubs is a fully managed streaming platform that can process millions of events per second. 
  - Event Hubs provides an endpoint for Apache Kafka, a widely used open-source stream-processing platform. 
  - When organizations use the endpoint feature, they don't need to build and maintain Kafka clusters for stream processing. 
  Instead, they can benefit from the fully managed Kafka implementation that Event Hubs offers.

- Azure Cosmos DB:
  - Azure Cosmos DB is a multi-model NoSQL database that offers multi-master replication. Azure Cosmos DB supports open-source APIs for many databases, languages, and platforms. For our requirement, it is to support Apache Cassandra.
  - Through the Azure Cosmos DB for Apache Cassandra, we can access Azure Cosmos DB data by using Apache Cassandra tools, languages, and drivers. Apache Cassandra is an open-source NoSQL database that's well suited for heavy write-intensive workloads.

- Kubernetes :
  - AKS is a highly available, secure, and fully managed Kubernetes service. Kubernetes is a rapidly evolving open-source platform for managing containerized workloads. AKS hosts open-source big data processing engines such as Apache Spark. By using AKS, you can run large-scale stream processing jobs in a managed environment.

- Postgres SQL :
  - Azure Database for PostgreSQL is a fully managed relational database service. It provides high availability, elastic scaling, patching, and other management capabilities for PostgreSQL. PostgreSQL is a widely adopted open-source relational database management system.

- Azure Cache :
  - Azure Cache for Redis provides an in-memory data store based on the Redis software. Redis is a popular open-source in-memory data store. Session stores, content caches, and other storage components use Redis to improve performance and scalability. Azure Cache for Redis provides open-source Redis capabilities as a fully managed offering.

### Best Practises :
Design and implement each service with best practices as follows :

- <b> Performance & Efficiency : </b>
  
  - Implement connection pooling for Azure Database for PostgreSQL. We can use a connection pooling library within the application. Or we can use a connection pooler such as PgBouncer or Pgpool. Establishing a connection with PostgreSQL is an expensive operation. With connection pooling, we can avoid degrading application performance. 
  - Configure Azure Cosmos DB for Apache Cassandra for best performance by using an appropriate partitioning strategy. Decide whether to use a single field primary key, a compound primary key, or a composite partition key when partitioning tables.
  - Maintenance of the environment and assets : Proper housekeeping activity need to performed by configuring business data retention period

- <b>Scalability : </b>

  - Need to streaming requirements into account when choosing an Event Hubs tier:
    - For mid-range throughput requirements of less than 120 MBps, consider the Premium tier. This tier scales elastically to meet streaming requirements.
    - For high-end streaming workloads with an ingress of gigabytes of data, consider the Dedicated tier. This tier is a single-tenant offering with a guaranteed capacity. You can scale dedicated clusters up and down.
    Consider autoscale-provisioned throughput for Azure Cosmos DB if your workloads are unpredictable and spiky. You can configure Azure Cosmos DB to use manually provisioned throughput or autoscale-provisioned throughput. With autoscale, Azure automatically and instantly scales the request units per second according to your usage.

- <b> Security : </b>
  
  - Use Azure Private Link to make Azure services part of your virtual network. When we use Private Link, traffic between the services and our network flows over the Azure backbone without traversing the public internet. The Azure services in this solution support Private Link for selected SKUs.
  - With Azure Cosmos DB for Apache Cassandra, keys provide access to resources like key spaces and tables. The Azure Cosmos DB instance stores those keys. Hence, keys need to rotated according to the organisation policy.
  - Use 256SHA encryption/decryption while <b> data in transit </b>. Data is stored by decrypting using public key.
  - Access privileges to be granted by admin by creating security group ID list. Alternativly, use of SSH key configure shorten the process and ideal for maintenance. Thereby, only user have access privileges are able to access the data.
  - PII data are masked by configuring in system table in Azure DB [Postgres SQL]

- <b> High availability & Resiliency: </b>

  - Use Availability zones to protect business-critical applications from datacenter failures. This solution's services support availability zones for selected SKUs in availability zone–enabled regions. For up-to-date information, review the list of services that support availability zones.

- <b> Cost optimization : </b>

  - Delect Event Hubs model from Basic / Standardv/ Premium tiers. The Premium or Dedicated tier is best for large-scale streaming workloads. 
  - It is best to scale throughput, so consider starting small and then scaling up as demand increases. 
    - Azure Cosmos DB offers two models: A provisioned throughput model that's ideal for demanding workloads. This model is available in two capacity management options: standard and autoscale. 
    - A serverless model that's well suited for running small, spiky workloads. 
    - An AKS cluster consists of a set of nodes, or virtual machines (VMs), that run in Azure. The cost of the compute, storage, and networking components make up a cluster's primary costs.
    - Azure Database for PostgreSQL can be selected based on compute nodes and storage capacity requirement.
    - Azure Cache for Redis tiers can be selected to min for intial run and scale-up as per the need.

- <b>  Fault Tolerant and Disaster Recovery : </b>

    - Image server should be located in another location (US/EU), if there is any disaster in South East Asia, image server can be switched as a part of disaster recovery.
    - Fault Tolerant & high availability :  Using sufficient cluster nodes for Database and load balancer for event hub and cache-memory for reporting applications

- <b> Latency </b> :

  - Data is processed real-time as well as for specific application on batch mode which is designed to handle with low latency.
