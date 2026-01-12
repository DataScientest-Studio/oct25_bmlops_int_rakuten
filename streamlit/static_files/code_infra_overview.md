# entire structure
---
config:
  layout: elk
  look: neo
---
flowchart TB
 subgraph CI["CI/CD"]
        git["Git Repo"]
        release["Milestone Pipeline"]
  end
 subgraph DS["Data Sources"]
        mongo["MongoDB"]
        postgres["PostgreSQL"]
  end
 subgraph ORCH["Airflow & Pipelines"]
        airflow["Airflow"]
        etl["ETL Pipeline"]
        sim["Similarity Matrix Pipeline"]
        rec["Recommendation Pipeline"]
  end
 subgraph API["API Layer"]
        api1["Trigger ETL"]
        api2["Trigger Similarity"]
        api3["Trigger Recommendation"]
  end
 subgraph EXP["MLflow Tracking"]
        mlflow["MLflow"]
  end
 subgraph MON["Monitoring"]
        prom["Prometheus"]
        graf["Grafana"]
        nodeexp["Node Exporter"]
  end
 subgraph DOCKER["Docker Compose"]
        d_airflow["airflow-docker"]
        d_api["api-docker"]
        d_ml["mlflow-docker"]
        d_mon["monitoring-docker"]
  end
    mongo --> etl
    etl --> sim
    sim --> rec & mlflow
    rec --> mlflow
    postgres --> airflow
    airflow --> etl & sim & rec
    api1 --> etl
    api2 --> sim
    api3 --> rec
    nodeexp --> prom
    prom --> graf
    git --> release
    release --> airflow
    d_airflow --> ORCH
    d_api --> API
    d_ml --> EXP
    d_mon --> MON

# databases
architecture-beta
  group data_sources(database)[Data Sources]

  service mongo(database)[MongoDB] in data_sources
  service postgres(database)[PostgreSQL] in data_sources

# Airflow orchestration and pipelines
architecture-beta
    group orchestration(server)[Airflow & Pipelines]

    service airflow(server)[Airflow] in orchestration
    service etl(server)[ETL Pipeline] in orchestration
    service similarity(server)[Similarity Matrix Pipeline] in orchestration
    service recommender(server)[Recommendation Pipeline] in orchestration

    airflow:T --> B:etl
    airflow:T --> B:similarity
    airflow:T --> B:recommender

# APIs
architecture-beta
    group apis(cloud)[API Layer]

    service api_trigger(cloud)[API: Trigger Pipelines] in apis

# MLflow tracking
architecture-beta
    group experiment_tracking(cloud)[MLflow Tracking]

    service mlflow(cloud)[MLflow] in experiment_tracking

# Monitoring
architecture-beta
    group monitoring(internet)[Monitoring Stack]

    service prometheus(internet)[Prometheus] in monitoring
    service grafana(internet)[Grafana] in monitoring
    service nodeexp(server)[Node Exporter] in monitoring

# CI/CD pipelines
architecture-beta
    group ci_cd(server)[CI/CD Pipeline]

    service git(server)[Git Repo] in ci_cd
    service release(server)[Milestone Pipeline] in ci_cd