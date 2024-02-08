workspace "DESI Tool" "Digital Decade DESI visualisation tool" {

    # softwareSystem <name> [description] [tags]
    # <identifier> -> <identifier> [description] [technology] [tags]

    properties {
        author "Andrei Meliș"
        version "1.0"
    }
    
    model {

        desi = softwareSystem "DESI Tool" "Digital Decade DESI visualisation tool." "DESI" {
            singlePageApplication = container "SPA" "Provides visualizations to public visitors." "Vue.js, Highcharts and ECL" "Web Browser"
            webServer = container "Web Server" "Delivers the static content and the single page application." "nginx"
            adminApplication = container "Admin Console" "Provides user interfaces for managing content and configuration." "Django"
            apiApplication = container "API Application" "Provides functionality via a JSON/HTTPS API." "Django REST framework"
            database = container "Database" "Stores configuration, statistical data and metadata, etc." "PostgreSQL" "Database"
            filesystem = container "File system" "Stores application files" "ext4" "File system"
        }

        visitor = person "Visitor" "Any visitor of the public website"
        webmaster = person "Administrator" "Application and data administrator" "EC"

        group "EC tools" {
            eurostat = softwareSystem "Eurostat" "Eurostat SDMX 2.1 Dissemination API" "EC"
            eulogin = softwareSystem "EU Login" "Single sign-on" "EC"
            ecl = softwareSystem "EC Webtools" "Europa Component Library" "EC"
            piwik = softwareSystem "Europa Analytics" "Web statistics" "EC"
        }

        group "EDW tools" {
            mailserver = softwareSystem "Mail system" "SMTP server" "EDW"
            zabbix = softwareSystem "Monitoring tool" "Zabbix" "EDW"
            wazuh = softwareSystem "SIEM" "Wazuh" "EDW"
            elk = softwareSystem "Log collection tool" "ELK" "EDW"
            restic = softwareSystem "Backup tool" "Restic" "EDW"
        }
        
        github = softwareSystem "GitHub" "VCS and CI/CD"
        aws = softwareSystem "AWS" "Amazon Web Services" "Amazon Web Services - Cloud" 

        # relationships between people and software systems
        visitor -> desi "Browses" "HTTPS"
        webmaster -> desi "Administers content and configuration" "HTTPS"
        
        # IT operations systems
        github -> desi "Deploys new versions"
        desi -> zabbix "Availability monitoring using"
        desi -> elk "Ships log files to"
        desi -> wazuh "Security monitoring using"
        desi -> restic "Is backed up using"
        desi -> aws "Is hosted in"

        # relationships to/from containers
        visitor -> webServer "Visits digital-decade-desi.digital-strategy.ec.europa.eu" "HTTPS"
        visitor -> singlePageApplication "Browses data and charts"
        webmaster -> webServer "Visits /admin" "HTTPS"
        webmaster -> adminApplication "Manages application settings and data"
        webServer -> singlePageApplication "Delivers to the visitor's web browser"
        singlePageApplication -> apiApplication "Fetches data from" "JSON/HTTPS"
        apiApplication -> database "Reads data from" "SQL/TCP"
        adminApplication -> database "Reads from and writes to" "SQL/TCP"
        adminApplication -> filesystem "Stores file uploads and images"
        webServer -> adminApplication "Serves web content from"
        webServer -> apiApplication "Serves JSON content from"
        webServer -> filesystem "Serves static content from"

        webmaster -> eulogin "Logs in" "CAS"
        adminApplication -> eulogin "Validates authentication" "CAS"
        adminApplication -> eurostat "Imports and transforms data from" "JSON/HTTPS"
        
        singlePageApplication -> piwik "Sends web statistics to" "HTTPS"
        singlePageApplication -> ecl "Loads web components from" "HTTPS"
        
        apiApplication -> mailserver "Sends email via" "SMTP"
        mailserver -> webmaster "Delivers email to" "SMTP"

        deploymentEnvironment "Production" {
            deploymentNode "Visitor's computer" "" {
                deploymentNode "Web Browser" "" "Chrome, Firefox, Safari, or Edge" {
                    liveSinglePageApplicationInstance = containerInstance singlePageApplication
                }
            }
            deploymentNode "Amazon Web services - cnect-desi-prod" {
                tags "Amazon Web Services - Cloud"
                region = deploymentNode "EU-North-1 (Stockholm)" {
                    tags "Amazon Web Services - Region"
                    deploymentNode t3.large" {
                        tags "Amazon Web Services - EC2 Instance"
                        deploymentNode "Host OS" "" "Ubuntu 22 LTS" {
                            deploymentNode "nginx" "" "nginx" {
                                webServerInstance = containerInstance webServer
                            }
                            deploymentNode "Docker engine" "" "Docker" {
                                deploymentNode "Docker container - application" "" "Django" {
                                    apiApplicationInstance = containerInstance apiApplication
                                    adminApplicationInstance = containerInstance adminApplication
                                }
                                deploymentNode "Docker container - database server" "" "PostgreSQL"{
                                    databaseInstance = containerInstance database
                                }
                                deploymentNode "Docker volume - application files" "" "File system"{
                                    filesystemInstanceApp = containerInstance filesystem
                                }
                            }
                        }
                    }
                }
            }
        }
        
    }
    
    views {
        systemContext desi "SystemContext" {
            include desi visitor webmaster eurostat eulogin ecl piwik mailserver
            autoLayout
        }

        systemLandscape desi_operational "Operational system landscape" {
            include desi zabbix elk restic github aws wazuh
            autoLayout
        }

        container desi "Containers" {
            include *
            autoLayout lr
            description "The container diagram for the DESI Tool."
        }
        
        container desi "Containers_simplified" {
            include *
            exclude ecl piwik eurostat
            autoLayout lr
            description "The container diagram for the DESI Tool."
        }

        deployment desi "Production" "DESI-Production"{
            include *
            autoLayout lr
            description "The production deployment diagram for DESI Tool."
        }

        theme https://static.structurizr.com/themes/amazon-web-services-2020.04.30/theme.json
        
        branding {
            logo https://eaudeweb.ro/images/edw-logo.png
        }
        styles {
            element "Software System" {
                background #ebebeb
                color #111111
                fontSize 36
            }
            element "DESI" {
                background #ffd617
                color #111111
            }
            element "EDW" {
                background #109e13
                color #eeeeee
            }
            element "EC" {
                background #082b7a
                color #eeeeee
            }
            element "Person" {
                shape person
                background #ebebeb
                color #111111
                fontSize 36
            }
            element "Group" {
                fontSize 36
            }
            element "Container" {
                fontSize 36
            }
            element "Web Browser" {
                shape WebBrowser
            }
            element "Mobile App" {
                shape MobileDeviceLandscape
            }
            element "Database" {
                shape Cylinder
            }
            element "File system" {
                shape Folder
            }
            relationship "Relationship" {
                fontSize 32
                color #222222
                style "dotted"
                routing "direct"
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
