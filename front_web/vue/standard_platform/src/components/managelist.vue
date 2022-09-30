   <template>

   <!-- <v-navigation-drawer> -->
    <v-card
        class="mx-auto"
        width="300"
      
    >
        <v-list>
        <v-list-item>
            <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
            </v-list-item-icon>

            <v-list-item-title>Ziipin</v-list-item-title>
        </v-list-item>

        <v-list-group
            :value="false"
            prepend-icon="mdi-account-circle"
        >
            <template v-slot:activator>
            <v-list-item-title>测试管理</v-list-item-title>
            </template>

            <v-list-group
            :value="false"
            no-action
            sub-group
            >
                <template v-slot:activator>
                    <v-list-item-content>
                    <v-list-item-title>测试执行管理</v-list-item-title>
                    </v-list-item-content>
                </template>

                        <v-list-item link to="/mainpage/testdata">
                            <v-list-item-title v-text="btn1"></v-list-item-title >

                            <v-list-item-icon>
                            <v-icon v-text="'mdi-account-multiple-outline'"></v-icon>
                            </v-list-item-icon>

                        </v-list-item>


                        <v-list-item link to="/mainpage/settings">
                            <v-list-item-title v-text="btn2"></v-list-item-title >

                            <v-list-item-icon>
                            <v-icon v-text="'mdi-cog-outline'"></v-icon>
                            </v-list-item-icon>

                        </v-list-item>
            </v-list-group>




            <v-list-group
            no-action
            sub-group
            >
            <template v-slot:activator>
                <v-list-item-content>
                <v-list-item-title>测试报告管理</v-list-item-title>
                </v-list-item-content>
            </template>

            <v-list-item
                v-for="([title, icon], i) in reports"
                :key="i"
                link to="/mainpage/reportdata"
            >
                <v-list-item-title v-text="title"></v-list-item-title>

                <v-list-item-icon>
                <v-icon v-text="icon"></v-icon>
                </v-list-item-icon>
            </v-list-item>
            </v-list-group>
        </v-list-group>
        </v-list>
    </v-card>
    <!-- </v-navigation-drawer> -->
    </template>


<script>
        export default {
            data: () => ({
                btn1:"测试数据相关",
                btn2:"设置",
        reports: [
            ['测试报告列表', 'mdi-plus-outline'],
            ['测试报告简要', 'mdi-file-outline'],
            ['图像数据', 'mdi-update'],
            ['垃圾箱', 'mdi-delete'],
            ],
            }),
        }
</script>