from App import App
from backup import backup
import sys

layout="""<TeamLayoutConfig>
  <layoutxml><finesseLayout xmlns="http://www.cisco.com/vtg/finesse">
    <!--  DO NOT EDIT. The version number for the layout XML. -->
    <version>1250.03</version>
    <configs>
        <!-- The Title for the application which can be customized. -->
        <config key="title" value="Cisco Finesse"/>
        <!-- The logo file for the application -->
        <!-- For detailed instructions on using custom icons for logos and tabs,
        please refer to the section "Customise Title and Logo in the Header"
        in the Finesse Administration Guide. -->
        <!-- <config key="logo" value="/3rdpartygadget/files/cisco_finext_logo.png"/>  -->
    </configs>
    <header>
        <!--  Please ensure that at least one gadget/component is present within every headercolumn tag -->
        <leftAlignedColumns>
            <headercolumn width="300px">
                <component id="cd-logo">
                    <url>/desktop/scripts/js/logo.js</url>
                </component>
            </headercolumn>
            <headercolumn width="230px">
                <component id="agent-voice-state">
                    <url>/desktop/scripts/js/agentvoicestate.component.js</url>
                </component>
            </headercolumn>
            <headercolumn width="251px">
                <component id="nonvoice-state-menu">
                    <url>/desktop/scripts/js/nonvoice-state-menu.component.js</url>
                </component>
            </headercolumn>
        </leftAlignedColumns>
        <rightAlignedColumns>
            <headercolumn width="50px">
                <component id="broadcastmessagepopover">
                    <url>/desktop/scripts/js/teammessage.component.js</url>
                </component>
            </headercolumn>
            <headercolumn width="50px">
                <component id="chat">
                    <url>/desktop/scripts/js/chat.component.js</url>
                </component>
            </headercolumn>
            <headercolumn width="50px">
                <component id="make-new-call-component">
                    <url>/desktop/scripts/js/makenewcall.component.js</url>
                </component>
            </headercolumn>
            <headercolumn width="72px">
                <component id="identity-component">
                    <url>/desktop/scripts/js/identity-component.js</url>
                </component>
            </headercolumn>
        </rightAlignedColumns>
    </header>
    <layout>
        <role>Agent</role>
        <page>
            <gadget>/desktop/scripts/js/callcontrol.js</gadget>
        </page>
        <tabs>
            <tab>
                <id>home</id>
                <icon>home</icon>
                <label>finesse.container.tabs.agent.homeLabel</label>
                <columns>
                    <column>
                        <gadgets>
                           <!-- <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=310&amp;viewId_1=99E6C8E210000141000000D80A0006C4&amp;filterId_1=agent.id=CL%20teamName&amp;viewId_2=9AB7848B10000141000001C50A0006C4&amp;filterId_2=agent.id=CL%20teamName</gadget>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=310&amp;viewId=B71A630C10000144000002480A0007C5&amp;filterId=precisionQueue.id=CL%20teamName</gadget>-->
                        </gadgets>
                    </column>
                </columns>
            </tab>
            <tab>
                <id>myHistory</id>
                <icon>history</icon>
                <label>finesse.container.tabs.agent.myHistoryLabel</label>
                <columns>
                    <column>
                        <gadgets>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=280&amp;viewId=5FA44C6F930C4A64A6775B21A17EED6A&amp;filterId=agentTaskLog.id=CL%20teamName</gadget>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=280&amp;viewId=56BC5CCE8C37467EA4D4EFA8371258BC&amp;filterId=agentStateLog.id=CL%20teamName</gadget>
                        </gadgets>
                    </column>
                </columns>
            </tab>
            <!-- <tab>
                <id>manageCustomer</id>
                <label>finesse.container.tabs.agent.manageCustomerLabel</label>
                <gadgets>
                    <gadget>/desktop/gadgets/CustomerContext.xml</gadget>
                </gadgets>
            </tab> -->
        </tabs>
    </layout>
    <layout>
        <role>Supervisor</role>
        <page>
            <gadget>/desktop/scripts/js/callcontrol.js</gadget>
        </page>
        <tabs>
            <tab>
                <id>home</id>
                <icon>home</icon>
                <label>finesse.container.tabs.supervisor.homeLabel</label>
                <columns>
                    <column>
                        <gadgets>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=310&amp;viewId=B71A630C10000144000002480A0007C5&amp;filterId=precisionQueue.id=CL%20teamName</gadget>
                            <gadget id="team-performance" maxRows="20">/desktop/scripts/js/teamPerformance.js</gadget>
                        </gadgets>
                    </column>
                    <!-- <column>
                        <gadgets>
                            <gadget staticMessage="select.agent.message">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=275&amp;viewId=630CB4C96B0045D9BFF295A49A0BA45E&amp;filterId=agentTaskLog.id=AgentEvent:Id&amp;type=dynamic&amp;maxRows=20</gadget>
                            <gadget staticMessage="select.agent.message">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=275&amp;viewId=56BC5CCE8C37467EA4D4EFA8371258BC&amp;filterId=agentStateLog.id=AgentEvent:Id&amp;type=dynamic&amp;maxRows=20</gadget>
                        </gadgets>
                     </column> -->
                </columns>
            </tab>
            <tab>
                <id>myHistory</id>
                <icon>history</icon>
                <label>finesse.container.tabs.agent.myHistoryLabel</label>
                <columns>
                    <column>
                        <gadgets>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=280&amp;viewId=5FA44C6F930C4A64A6775B21A17EED6A&amp;filterId=agentTaskLog.id=CL%20teamName</gadget>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/LiveData/LiveDataGadget.xml?gadgetHeight=280&amp;viewId=56BC5CCE8C37467EA4D4EFA8371258BC&amp;filterId=agentStateLog.id=CL%20teamName</gadget>
                        </gadgets>
                    </column>
                </columns>
            </tab>
            <tab>
                <id>teamData</id>
                <icon>team-data</icon>
                <label>finesse.container.tabs.supervisor.teamDataLabel</label>
                <columns>
                    <column>
                        <!-- The following gadget is used by the supervisor to view an agent&apos;s queue interval details.  -->
                        <gadgets>
                            <gadget alternateHosts="AAA">https://XYZ:8444/cuic/gadget/Historical/HistoricalGadget.xml?viewId=BD9A8B7DBE714E7EB758A9D472F0E7DC&amp;linkType=htmlType&amp;viewType=Grid&amp;refreshRate=900&amp;@start_date=RELDATE%20THISWEEK&amp;@end_date=RELDATE%20THISWEEK&amp;@agent_list=CL%20~teams~&amp;gadgetHeight=360</gadget>
                        </gadgets>
                    </column>
                </columns>
            </tab>
            <!-- <tab>
            	<id>queueData</id>
                <label>finesse.container.tabs.supervisor.queueDataLabel</label>
                <columns>
                	<column>
                		<gadgets>
                            <gadget>/desktop/scripts/js/queueStatistics.js</gadget>
                		</gadgets>
                	</column>
                </columns>
            </tab> -->
            <!-- <tab>
                <id>manageCustomer</id>
                <label>finesse.container.tabs.supervisor.manageCustomerLabel</label>
                <gadgets>
                    <gadget>/desktop/gadgets/CustomerContext.xml</gadget>
                </gadgets>
            </tab> -->
        </tabs>
    </layout>
</finesseLayout>
</layoutxml>
  <useDefault>true</useDefault>
</TeamLayoutConfig>

"""
def tester():
    """Test program for Finesse Layout update.
    Usage: python App.py [-d] ... [finessepub [username [password]]]
    """
    print("##### Inputs received from command prompt %s #####" %(sys.argv[1:]))
    if sys.argv[1]=="-d" and len(sys.argv[1:5])==4:
        finessePub = ""
        if sys.argv[1:]:
            finessePub = sys.argv[2]

        username = ""
        if sys.argv[2:]:
            username = sys.argv[3]

        password=""
        if sys.argv[3:]:
            password = sys.argv[4]

        takebackup=False
        if len(sys.argv[1:])==5:
            backup = sys.argv[5]
            if backup=="takebackup":
                takebackup=True
        try:
            if takebackup:
                print("##### enable layout backup workflow #####")
            else:
                print("##### enable layout update workflow #####")
            a= App(finessePub,username,password,takebackup)
            print("##### Application Initialized #####")
            a._run()
        except Exception as e:
            print("#### exception while initializing Application : %s ####" %(e))
            sys.exit(1)
    else:
        print("#### exception while initializing Application : %s ####" %("""Usage for backup: python App.py -d finessepub  username  password takebackup"""))
        print("#### exception while initializing Application : %s ####" %("""Usage: python App.py -d finessepub  username  password """))

        sys.exit(1)

if __name__ == "__main__":
    #tester()
    msg = backup.output_to_file("5802",layout)
    print(msg)
