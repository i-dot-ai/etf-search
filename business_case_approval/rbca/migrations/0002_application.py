# Generated by Django 3.2.16 on 2022-10-07 08:50

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rbca", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=127)),
                ("hrbp", models.CharField(blank=True, max_length=127, null=True)),
                (
                    "grade",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("AA", "AA"),
                            ("AO", "AO"),
                            ("EO", "EO"),
                            ("HEC", "HEC"),
                            ("SEO", "SEO"),
                            ("G7", "G7"),
                            ("G6", "G6"),
                            ("SC_S1", "SCS1"),
                            ("SC_S2", "SCS2"),
                            ("SC_S3", "SCS3"),
                            ("PERM_SEC", "Perm Sec"),
                            ("FAST_STREAM", "Fast stream"),
                            ("TI_S1", "TIS1"),
                            ("TI_S2", "TIS2"),
                            ("TI_S3", "TIS3"),
                            ("PUBLIC_APPOINTMENT", "Public Appointment"),
                            ("SPECIAL_ADVISOR", "Special Advisor"),
                            ("MINISTER", "Minister"),
                            ("PC", "PC"),
                            ("DPC", "DPC"),
                            ("SAPC", "SAPC"),
                            ("APC", "APC"),
                            ("SENIOR_COMMERCIAL", "Senior Commercial"),
                            ("COMMERCIAL_SPECIALIST", "Commercial Specialist"),
                            ("ASSOCIATE_COMMERCIAL_SPECIALIST", "Associate Commercial Specialist"),
                            ("COMMERCIAL_LEAD", "Commercial Lead"),
                            ("CROWN_REPRESENTIATIVE", "Crown Representiative"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=127, null=True)),
                (
                    "business_unit_1",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PRIME_MINISTERS_OFFICE", "Prime Minister's Office"),
                            (
                                "OFFICE_FOR_SCIENCE_AND_TECHNOLOGY_STRATEGY",
                                "Office for Science and Technology Strategy",
                            ),
                            ("CABINET_SECRETARY_GROUP", "Cabinet Secretary Group"),
                            ("GOVERNMENT_IN_PARLIAMENT", "Government in Parliament"),
                            ("INTELLIGENCE_SECURITY_COMMITTEE", "Intelligence Security Committee"),
                            ("UNION_AND_CONSTITUTION_GROUP", "Union and Constitution Group"),
                            ("COP_PRESIDENCY", "COP Presidency"),
                            ("INQUIRIES_SPONSORSHIP_TEAM", "Inquiries Sponsorship Team"),
                            ("PLANNING_AND_ANALYSIS_SECRETARIAT", "Planning and Analysis Secretariat"),
                            ("NO_10_COMMUNICATIONS", "No.10 Communications"),
                            ("ECONOMIC_AND_DOMESTIC_SECRETARIAT", "Economic and Domestic Secretariat"),
                            ("NATIONAL_SECURITY_SECRETARIAT", "National Security Secretariat"),
                            ("JOINT_INTELLIGENCE_ORGANISATION", "Joint Intelligence Organisation"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "business_unit_2",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PRIME_MINISTERS_OFFICE", "Prime Minister's Office"),
                            (
                                "OFFICE_FOR_SCIENCE_AND_TECHNOLOGY_STRATEGY",
                                "Office for Science and Technology Strategy",
                            ),
                            ("CABINET_SECRETARY_GROUP", "Cabinet Secretary Group"),
                            ("GOVERNMENT_IN_PARLIAMENT", "Government in Parliament"),
                            ("INTELLIGENCE_SECURITY_COMMITTEE", "Intelligence Security Committee"),
                            ("UNION_AND_CONSTITUTION_GROUP", "Union and Constitution Group"),
                            ("COP_PRESIDENCY", "COP Presidency"),
                            ("INQUIRIES_SPONSORSHIP_TEAM", "Inquiries Sponsorship Team"),
                            ("PLANNING_AND_ANALYSIS_SECRETARIAT", "Planning and Analysis Secretariat"),
                            ("NO_10_COMMUNICATIONS", "No.10 Communications"),
                            ("ECONOMIC_AND_DOMESTIC_SECRETARIAT", "Economic and Domestic Secretariat"),
                            ("NATIONAL_SECURITY_SECRETARIAT", "National Security Secretariat"),
                            ("JOINT_INTELLIGENCE_ORGANISATION", "Joint Intelligence Organisation"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                ("establishment", models.TextField(blank=True, null=True)),
                ("impact_statement", models.TextField(blank=True, null=True)),
                ("ddat_role", models.BooleanField(blank=True, null=True)),
                (
                    "ddat_family",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("DATA", "Data"),
                            ("IT_OPERATIONS", "IT operations"),
                            ("PRODUCT_AND_DELIVERY", "Product and delivery"),
                            ("QUALITY_ASSURANCE_TESTING_QAT", "Quality assurance testing (QAT)"),
                            ("TECHNICAL", "Technical"),
                            ("USER_CENTRED_DESIGN", "User-centred design"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "funding_source",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("OGD", "OGD"),
                            ("RECHARGE", "Recharge"),
                            ("PROGRAMME", "Programme"),
                            ("OTHER", "Other"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "recruitment_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("CONTINGENT_LABOUR", "Contingent Labour"),
                            ("CONTINGENT_LABOR_EXTENSION", "Contingent Labor Extension"),
                            ("CROWN_REPRESENTATIVE", "Crown Representative"),
                            ("FTA", "FTA"),
                            ("LOAN", "Loan"),
                            ("LOAN_EXTENSION", "Loan Extension"),
                            ("MANAGED_MOVE", "Managed Move"),
                            ("PERMANENT", "Permanent"),
                            ("SECONDMENT", "Secondment"),
                            ("SECONDMENT_EXTENSION", "Secondment Extension"),
                            ("STFTA", "STFTA"),
                            ("TDA", "TDA"),
                            ("DA_EXTENSION", "DA extension"),
                            ("TEMPORARY_POST", "Temporary post"),
                            ("OTHER", "Other"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "recruitment_mechanism",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("CONTINGENT_LABOUR", "Contingent Labour"),
                            ("CONTINGENT_LABOR_EXTENSION", "Contingent Labor Extension"),
                            ("EOI_CO", "EOI CO"),
                            ("EXTERNAL_RECRUITMENT", "External Recruitment"),
                            ("FTA", "FTA"),
                            ("FTA_EXTENSION", "FTA Extension"),
                            ("X_CS", "X-CS"),
                            ("LOAN_EXTENSION", "Loan Extension"),
                            ("PERMANENCY_REQUEST", "Permanency Request"),
                            ("SECONDMENT", "Secondment"),
                            ("SECONDMENT_EXTENSION", "Secondment Extension"),
                            ("TP_TDA", "TP/TDA"),
                            ("TP_TDA_EXTENSION", "TP/TDA Extension"),
                            ("N_A", "N/A"),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "locations",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True,
                            choices=[
                                ("GLASGOW", "Glasgow"),
                                ("BELFAST", "Belfast"),
                                ("CARDIFF", "Cardiff"),
                                ("EDINBURGH", "Edinburgh"),
                                ("MANCHESTER", "Manchester"),
                                ("BRISTOL", "Bristol"),
                                ("YORK", "York"),
                                ("NORWICH", "Norwich"),
                                ("BASINGSTOKE", "Basingstoke"),
                                ("NEWCASTLE", "Newcastle"),
                                ("MILTON_KEYNES", "Milton Keynes"),
                                ("BIRMINGHAM", "Birmingham"),
                                ("LONDON", "London"),
                            ],
                            max_length=127,
                            null=True,
                        ),
                        size=None,
                    ),
                ),
                ("location_strategy", models.BooleanField(blank=True, null=True)),
                (
                    "london_reason",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "MINISTER_SUPPORT",
                                "Be in direct support of ministers and are expected to meet with ministers personally as part of their core daily tasks, eg private secretaries, permanent secretaries, and their offices.",
                            ),
                            (
                                "BUSINESS_NEEDS",
                                "Require a London presence to satisfy essential business needs / are public-facing operational delivery roles serving the London population.",
                            ),
                            (
                                "SPECIALIST_FACILITIES",
                                "Require specialist facilities that would be prohibitivelv expensive to re-establish elsewhere.",
                            ),
                        ],
                        max_length=127,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
