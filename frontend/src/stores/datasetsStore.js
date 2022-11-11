import { defineStore } from "pinia";

export default defineStore("dataset", {
  state: () => {
    return {
      datasets: [
        {
          code: "desi",
          name: "Digital Economy and Society Index",
          short_name: "DESI",
          description:
            "The Digital Economy and Society Index (DESI) is a composite index that summarises relevant indicators on Europe’s digital performance and tracks the evolution of EU Member States, across five main dimensions: Connectivity, Human Capital, Use of Internet, Integration of Digital Technology, Digital Public Services. Read reports and methodological notes.",
        },
        {
          code: "key_indicators",
          name: "Key Indicators",
          short_name: "Key Indicators",
          description:
            "European Commission services selected various indicators, divided into thematic groups, which illustrate some key dimensions of the European information society (Telecom sector, Broadband, Mobile, Internet usage, Internet services, eGovernment, eCommerce, eBusiness, ICT Skills, Research and Development). These indicators allow a comparison of progress across European countries as well as over time. Multiple interactive charts allow you to assess countries' profiles.",
        },
        {
          code: "e-gov-2020",
          name: "e-Government Benchmark (from 2020 onwards)",
          short_name: "E-Gov-2020",
          description:
            "The e-Government Benchmark framework corresponds with the key policy priorities in the e-government Action Plan, the Tallinn and Berlin Declarations. The e-Government Benchmark framework reflects on the Digital Decade and it brings insights on the state-of play of e-government in Europe. The measurement evaluates the maturity of online public services in terms of User centricity, Transparency, and use of Key enablers. It also brings the dimension of Cross-border service delivery, which is a truly European metric. The new method presents various changes e.g. simplified life events by measuring less services for national users, substantially increasing the amount of services that are measured cross-border, including the Career and the Family life events, and addition of Health life events for odd years together with relabeling of some indicators. Various indicators allow the comparison over the time and across countries. The list of countries currently includes the European Union Member States, Iceland, Norway, Montenegro, Republic of Serbia, Switzerland, Turkey as well as Albania and North Macedonia.",
        },
        {
          code: "e-gov",
          name: "e-Government Benchmark (2013-2019)",
          short_name: "E-Gov",
          description:
            "The e-Government Benchmark framework corresponds with the key policy priorities in the e-government Action Plan and the Tallinn Declaration and brings insights on the state-of play of e-government in Europe. The measurement evaluates the maturity of online public services in terms of User centricity, Transparency, and use of Key enablers. It also brings the dimension of Cross-border service delivery, which is a truly European metric. Various indicators allow the comparison over the time and across countries. The list of countries currently includes the European Union Member States, Iceland, Norway, Montenegro, Republic of Serbia, Switzerland, Turkey as well as Albania and North Macedonia.",
        },
      ],
    };
  },
  actions: {},
});
